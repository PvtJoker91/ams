<template>    
    <div class="space-y-3">
        <h2 class="text-3xl font-bold mb-4">Создание заявки в архив</h2>
        <div class="p-6 bg-white border border-gray-200 rounded-lg">
            <form @submit.prevent="saveRequest()">
                <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                    <div class="sm:col-span-2">
                    <label for="first-name" class="block text-sm font-medium leading-6 text-gray-900">Заказчик</label>
                    <div class="mt-2">
                        <input type="text"  v-model="request.client" required 
                        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                    </div>
                    </div>

                    <div class="sm:col-span-3">
                    <label for="last-name" class="block text-sm font-medium leading-6 text-gray-900">Подразделение заказчика</label>
                    <div class="mt-2">
                        <input type="text" v-model="request.client_department" required
                        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                    </div>
                    </div>

                    <div class="sm:col-span-3">
                    <label for="country" class="block text-sm font-medium leading-6 text-gray-900">Услуга (выбрать)</label>
                    <div class="mt-2">
                        <select id="service" v-model="request.service" required
                        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6">
                            <option v-for="service in services" v-bind:value="service.id">{{service.type}}</option>
                        </select>
                    </div>
                    </div>

                    <div class="sm:col-span-3">
                    <label for="country" class="block text-sm font-medium leading-6 text-gray-900">Срочность (выбрать)</label>
                    <div class="mt-2">
                        <select id="urgency" v-model="request.urgency" required
                        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6">
                            <option v-for="urgency in urgencys" v-bind:value="urgency.hours">{{urgency.type}}</option>
                        </select>
                    </div>
                    </div>

                    <div class="sm:col-span-5">
                    <label for="last-name" class="block text-sm font-medium leading-6 text-gray-900">Описание</label>
                    <div class="mt-2">
                        <textarea type="text" v-model="request.description" required
                        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                        </textarea>
                    </div>
                    </div>

                </div>
                <div class="mt-6 flex items-center gap-x-6">
                    <button type="submit"
                    class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Создать</button>
                </div>
            </form>
        </div>
    </div>


  </template>
  
  
  <script>
  import axios from 'axios'

  import { useUserStore } from '../../stores/user'
  
  export default{
    setup() {
        const userStore = useUserStore()

        return {
            userStore,
        }
    },
    
    data(){
        return{
        services:[
                  {type:'Сканирование в один файл', id:'full_scanning'},
                  {type:'Сканирование по документам', id:'scanning_by_documents'},
                  {type:'Выдача во временное пользование', id:'temporary_issuance'},
                  {type:'Безвозвратная выдача', id:'unrecoverable_issuance'},
              ],
        urgencys:[
                  {type:'Стандартная - 40 р.ч.', hours:40},
                  {type:'Повышенная - 16 р.ч.', hours:16},
                  {type:'Срочная - 8 р.ч.', hours:8},
              ],             

        request:{
            'status':'',
            'creator':'',
            'client':'',
            'client_department':'',
            'service':'',
            'urgency':'',
            'description':'',
            'dossiers':[]
        },
  
        'errArray': [],
        }
    },
  
    methods: {
    saveRequest(){
      this.request.creator = this.userStore.user.id;
      this.request.status = 'creation';
      axios.post('/api/requests/requests/', this.request
                            ).then(response =>{
                                    console.log(response.data)
                                    this.$router.push({
                                        name:'requestDetail',
                                        params: {id: response.data.id}
                                    })
                                    
                                    }         
                        ).catch(error =>{
                            console.log(error)
                        }
                        )

    },
    }
  
  }
  </script> 
  
    