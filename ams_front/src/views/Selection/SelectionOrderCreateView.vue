<template>
    <div v-if="userStore.user.isAuthenticated && userStore.user.id">
    <h2 class="text-3xl font-bold mb-8">Создать наряд на подбор</h2>
        <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
        <table v-if="!showForm" class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Этаж
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Просроченные
                    </th>
                    <th scope="col" class="px-6 py-3">
                        T+2ч 
                    </th>
                    <th scope="col" class="px-6 py-3">      
                        Сегодня 
                    </th>
                    <th scope="col" class="px-6 py-3">
                        T+1д
                    </th>
                    <th scope="col" class="px-6 py-3">
                        T+3д
                    </th>
                    <th scope="col" class="px-6 py-3">
                        T+7д
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Остальные
                    </th>
                </tr>
            </thead>
            <tbody v-if="tasks.length!==0">
                <tr v-for="(location, locationName) in timedLocatedTasks" :key="locationName" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <th scope="row" class="px-6 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        <div class="flex items-center">
                            <input 
                            type="checkbox" 
                            :id="'checkbox-' + locationName" v-model="checkedItems[locationName]" 
                            @change="handleCheckboxChange(locationName)"
                            class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                            <label :for="'checkbox-' + locationName" class="sr-only">{{ location }}</label>
                        </div>
                    </th>
                    <td class="px-6 py-3">
                        {{ locationName }}
                    </td>
                    <td class="px-6 py-3">
                        {{ location.outdated.length }}
                    </td>
                    <td class="px-6 py-3">
                        {{ location.h2.length }}
                    </td>
                    <td class="px-6 py-3">
                        {{ location.today.length }}
                    </td>
                    <td class="px-6 py-3">
                        {{ location.d1.length }}
                    </td>
                    <td class="px-6 py-3">
                        {{ location.d3.length }}
                    </td>
                    <td class="px-6 py-3">
                        {{ location.d7.length }}
                    </td>
                    <td class="px-6 py-3">
                        {{ location.rest.length }}
                    </td>
                </tr>
            </tbody>
            <button v-if="tasksToSelect.length!=0" @click="showForm=!showForm" 
            class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                     Создать наряд
            </button>
        </table>
        <div v-if="showForm" class="p-6 bg-white border border-gray-200 rounded-lg">
            <form @submit.prevent="saveOrder()">
                
                <h2 class="block text-xl font-medium leading-6 text-gray-900">Выбрано досье к выемке:  {{ tasksToSelect.length }}</h2>
                <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">

                    <div class="sm:col-span-3">
                    <label class="block text-sm font-medium leading-6 text-gray-900">Исполнитель (выбрать):</label>
                    <div class="mt-2">
                        <select id="executor" v-model="selectionOrder.executor" required
                        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6">
                            <option v-for="user in users" v-bind:value="user.id">{{user.last_name}} {{user.first_name}}</option>
                        </select>
                    </div>
                    </div>

                </div>
                <div class="mt-6 flex items-center gap-x-6">
                    <button @click="showForm=false"
                    class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                        Назад  
                    </button>
                    <button type="submit"
                    class="rounded-md bg-green-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                        Создать  
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
    <div v-else>
      <AccessDenied />
    </div>
    
  </template>
    
    
<script>
import axios from 'axios'
import AccessDenied from '../../components/AccessDenied.vue';
import { useUserStore } from '../../stores/user'

export default{

    components: {
    AccessDenied,
},

  setup() {
    const userStore = useUserStore()
      return {
        userStore
      }
  },

  data(){
      return{
        tasks: [],
        timedLocatedTasks: {
                 location:{
                    outdated: [],
                    h2: [],
                    today: [],
                    d1: [],
                    d3: [],
                    d7: [],
                    rest: [],
            }
        },
        selectionOrder:{
            creator:"",
            executor:"",
            tasks:""
        },
        tasksToSelect:[],
        checkedItems: [],
        showForm: false,
    }
  },
  async mounted() {
    await this.loadTasks();
    this.getTimedLocatedTasks(this.tasks)
    this.loadUsers()
  },

  methods: {
    loadUsers(){
        axios.get('/api/users/list/',
                    ).then(response =>{
                            console.log(response.data)
                            this.users = response.data
                            }         
                ).catch(error =>{
                    console.log(error)
                })
    },
    async loadTasks() {
      try {
        const response = await axios.get('/api/selection/tasks/');
        this.tasks = response.data;
        console.log(this.tasks);
      } catch (error) {
        console.log(error);
      }
    },

    getTimedLocatedTasks(obj){
        let timedLocatedObj = {};
        obj.forEach(task =>{
            const category = this.getCategory(task.hours_left); 
            const location = task.location;
            if (location) {
                const floor = location.slice(3, 5);
                if (!timedLocatedObj[floor]) {
                    timedLocatedObj[floor] = {
                                        outdated: [],
                                        h2: [],
                                        today: [],
                                        d1: [],
                                        d3: [],
                                        d7: [],
                                        rest: [],
                                    }
                                }      
                timedLocatedObj[floor][category].push(task)
            } else {
                if (!timedLocatedObj['unlocated']) {
                timedLocatedObj['unlocated']={
                                        outdated: [],
                                        h2: [],
                                        today: [],
                                        d1: [],
                                        d3: [],
                                        d7: [],
                                        rest: [],
                                    }
                                }
                timedLocatedObj['unlocated'][category].push(task)
            }
        })
        this.timedLocatedTasks = timedLocatedObj
        
    },

    getCategory(hoursLeft) {
        const hours = parseInt(hoursLeft);
        if (hours < 0) return 'outdated';
        if (hours <= 2) return 'h2';
        if (hours <= 8) return 'today';
        if (hours <= 24 * 1) return 'd1';
        if (hours <= 24 * 3) return 'd3';
        if (hours <= 24 * 7) return 'd7';
        return 'rest';
    },

    getTasksToSelect(location){        
        let tasks = []
        Object.keys(location).forEach((name) => {
            let time = location[name]
            if (time.length !==0){
            for(let i=0; i<time.length; i++) {
                let task = time[i]
                tasks.push(task.id)
                }
            }
        })
        return tasks
    },
    

    handleCheckboxChange(locationName) {
      let tasks = this.getTasksToSelect(this.timedLocatedTasks[locationName])
      if(this.checkedItems[locationName]){
        this.tasksToSelect.push(...tasks)
    } else { 
        this.tasksToSelect = this.tasksToSelect.filter(item => !tasks.includes(item))
      }
    },

    filterTasks(){
        this.tasks = this.tasks.filter(obj =>!this.tasksToSelect.includes(obj.id));
        this.getTimedLocatedTasks(this.tasks);
        this.tasksToSelect = [];
    },

    saveOrder(){
      this.selectionOrder.creator = this.userStore.user.id;
      this.selectionOrder.tasks = this.tasksToSelect;
      axios.post('/api/selection/orders/', this.selectionOrder
                            ).then(response =>{
                                    console.log(response.data)
                                    this.filterTasks()
                                    this.showForm = false
                                    }         
                        ).catch(error =>{
                            console.log(error)
                        })
    },
  }

}
</script> 