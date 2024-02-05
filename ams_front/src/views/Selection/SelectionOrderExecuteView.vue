<template>
    <div class="space-y-3">
      <h2 class="text-3xl font-bold mb-4">Исполнение нарядов</h2>
  
        <div class="p-6 bg-white border border-gray-200 rounded-lg">
            <div class="p-1 bg-white  rounded-lg">
                <form @submit.prevent="selectDossier()" class="flex items-center">
                    <label class="form-label mr-2">Введите ш/к досье</label>
                    <input type="text" class="form-control border border-gray-300 rounded-lg px-2 py-1 mr-8" v-model="dossier.barcode">
                    <span class="danger">{{ errArray['status_error'] ? errArray['status_error'].toString() : '' }}</span>
                    <span class="danger">{{ errArray['non_field_errors'] ? errArray['non_field_errors'].toString() : '' }}</span>
                    <span class="danger">{{ errArray['detail'] ? errArray['detail'].toString() : '' }}</span>
                    <span class="danger">{{ errArray['validation_error'] ? errArray['validation_error'].toString() : '' }}</span>
                    <span id='err' class="danger"></span>
                </form>
            </div>     
        </div>
  
        <div v-if="Object(this.registries).length !==0" class="relative overflow-x-auto shadow-md sm:rounded-lg">
            <h2 class="text-xl font-bold mb-2">Реестры в сектор исполнения запросов:</h2>
          <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
              <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                  <tr>
                      <th scope="col" class="px-6 py-3">
                          N
                      </th>
                      <th scope="col" class="px-6 py-3">
                          Тип реестра
                      </th>
                      <th scope="col" class="px-6 py-3">
                          Дата создания
                      </th>
                      <th scope="col" class="px-6 py-3">
                          Количество досье
                      </th>
                      <th scope="col" class="px-6 py-3">
                        <span class="sr-only">Отправить</span>
                    </th>
                  </tr>
              </thead>
              <tbody>
                  <tr v-for="registry, num in registries" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                      <th scope="row" class="px-6 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{ num + 1 }}
                      </th>
                      <td class="px-6 py-3">
                        {{ registry.type }}
                      </td>
                      <td class="px-6 py-3">
                        {{ registry.time_create }}
                      </td>
                      <td class="px-6 py-3">
                        {{ registry.dossiers.length }}
                      </td>
                      <td class="px-6 py-3">
                        <button @click="sendRegistry(registry)"
                        class="rounded-md bg-green-500 px-2 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-green-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                        Отправить  
                    </button>
                      </td>
                  </tr>
              </tbody>
          </table>
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
            userStore
        }
    },
  
    data(){
        return{
        registries:[],
        'dossier':{
            'barcode':'',
            'status':'Selected',
            'archive_box':null
        },
        'errArray': [],
        }
    },
    
    methods: {
    
        selectDossier(){
        axios.patch('/api/selection/dossier/' + this.dossier.barcode + '/', this.dossier).then(
            response =>{
                console.log(response.data)
                this.addRegistry(response.data.registries)
                this.dossier.barcode = ''
                this.errArray = []
            }
        ).catch(error =>{
            if (error.response) {
                console.log(error.response.data);
                this.errArray = error.response.data;
                }
            })
        },

        addRegistry(registries) {
            for (let i = 0; i < registries.length; i++) {
                let registry = registries[0];
                let isElementPresent = false;
                for (let j = 0; j < this.registries.length; j++) {
                    if (this.registries[j].id === registry.id) {
                        isElementPresent = true;
                        if(this.registries[j].dossiers.length!==registry.dossiers.length){
                            this.registries[j].dossiers=registry.dossiers
                        }
                        break;
                    }
                }
                if (!isElementPresent) {
                    this.registries.push(registry);
                }
            }
        },

        sendRegistry(registry){
            registry.status = 'sent';
            registry.sender = this.userStore.user.id
            axios.patch('/api/units/registry/' + registry.id + '/', registry).then(
                response =>{
                    console.log(response.data);
                    this.registries = [];
                }
            ).catch(error =>{
                if (error.response) {
                    console.log(error.response.data);
                    this.errArray = error.response.data;
                    }
                })
            },
        
    }
}
</script> 