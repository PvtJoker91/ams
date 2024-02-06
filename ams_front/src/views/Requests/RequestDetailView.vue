<template>
    <div v-if="userStore.user.isAuthenticated && userStore.user.id" class="space-y-3">
        <div v-if="Object.keys(currentRequest).length!==0">
        <h2 class="text-3xl font-bold mb-4">Заявка №{{ currentRequest.id }}  {{ currentRequest.time_create }}</h2>
            <div class="p-8 bg-white rounded-lg">
                <div v-if="currentRequest.status == 'creation'" class="flex items-center">
                    <button class="mr-4 rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500" 
                         @click="showSearch=false">Детали заявки
                    </button>
                    <button class="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500" 
                        @click="showSearch=true, errArray=[]">Добавить досье
                        <span class="inline-flex items-center justify-center w-4 h-4 ms-2 text-xs font-semibold text-blue-800 bg-blue-200 rounded-full">
                            {{ addedDossiers.length }}
                        </span>
                    </button>
                </div>

                <div v-if="!this.showSearch" class="flex mt-3" >
                    <div class="flex-1">
                        <h2 class="text-xl font-bold mb-4">Реквизиты заявки:</h2>
                        <div class="container mx-auto grid grid-cols-2 gap-4">
                            <div>
                                <b class="block">Заказчик: </b>
                                <span class="block">{{ currentRequest.client }}</span>
                            </div>
                            <div>
                                <b class="block">Подразделение заказчика: </b>
                                <span class="block">{{ currentRequest.client_department }}</span>
                            </div>
                            <div>
                                <b class="block">Создатель заявки: </b>
                                <span class="block">{{ currentRequest.creator.first_name }} {{ currentRequest.creator.last_name }}</span>
                            </div>
                            <div>
                                <b class="block">Услуга: </b>
                                <span class="block">{{ currentRequest.service }}</span>
                            </div>
                            <div>
                                <b class="block">Срочность: </b>
                                <span class="block">{{ currentRequest.urgency }}</span>
                            </div>
                            <div v-if="currentRequest.time_create!==null">
                                <b class="block">Дата создания: </b>
                                <span class="block">{{ currentRequest.time_create }}</span>
                            </div>
                            <div v-if="currentRequest.time_close!==null">
                                <b class="block">Дата закрытия: </b>
                                <span class="block">{{ currentRequest.time_close }}</span>
                            </div>
                            <div>
                                <b class="block">Статус: </b>
                                <span class="block">{{ currentRequest.status }}</span>
                            </div>
                            <div>
                                <b class="block">Описание: </b>
                                <span class="block">{{ currentRequest.description}}</span>
                            </div>
                            <div v-if="currentRequest.close_reason!==null">
                                <b class="block">Причина закрытия: </b>
                                <span class="block">{{ currentRequest.close_reason}}</span>
                            </div>
                            <div v-if="currentRequest.closer!==null">
                                <b class="block">Исполнитель: </b>
                                <span class="block">{{ currentRequest.closer.first_name }} {{ currentRequest.closer.last_name }}</span>
                            </div>
                        </div>

                    
                    <div class="flex items-center">    
                        <div v-if="currentRequest.status == 'sent_for_processing' && !hasGroup('Не сотрудники архива')" class="flex items-center">
                            <button @click="requestAccept()" class="float-left ml-2 mt-4 rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-500" >
                                Подтвердить заявку
                            </button>
                        </div>

                    
                        <div v-if="this.addedDossiers.length !==0 && currentRequest.status == 'creation'">
                            <button @click="requestSend()" class="float-left ml-2 mt-4 rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-500">
                                    Отправить заявку
                            </button>
                        </div>
                            
                        <div v-if="currentRequest.status == 'creation'">
                            <button @click="requestDelete()" class="float-left ml-2 mt-4 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500">
                                Удалить заявку
                            </button>
                        </div>
                        
                        <div v-if="currentRequest.status !== 'creation' && currentRequest.status !== 'cancelled' && currentRequest.status !== 'complete'">
                            <button v-if="!showDialog" @click="showDialog=true" class="float-left ml-2 mt-4 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500">
                                Закрыть заявку
                            </button>
                            <div v-if="showDialog" class="ml-6">
                                <p>Введите причину закрытия</p>
                                <div class="flex items-center">
                                    <input v-model="currentRequest.close_reason">
                                    <button @click="requestCancel()" class="float-left ml-2 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500">
                                        Закрыть
                                    </button>
                                    <button @click="showDialog=false, currentRequest.close_reason=null" class="float-left ml-2 rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500">
                                        Отмена
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex-1">
                        <div v-if="Object(addedDossiers).length!==0">
                            <h2 class="text-xl font-bold mb-4">Досье в заявке:  ({{ addedDossiers.length }})</h2>
                            <li v-for="dossier in addedDossiers">

                                <RouterLink :to="{name: 'dossierScans', params:{'barcode': dossier.barcode}}" target="_blank" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">
                                    {{ dossier.barcode }}
                                </RouterLink>


                                <a v-if="currentRequest.status !== 'creation'">   ({{ dossier.scan_count }})</a>
                                <button v-if="currentRequest.status == 'creation'"
                                @click="addRemoveDossierToRequest(dossier)" class="ml-3 rounded-md bg-indigo-600 px-1 py-0.2 text-xs font-semibold text-white shadow-sm hover:bg-indigo-500">
                                    Remove
                                </button>
                            </li>
                        </div>
                    </div>
                </div>         
            
                <div v-if="this.showSearch" class="ml-2">
                    <div v-if="Object(foundDossiers).length==0"  class="mt-5">
                        <div class="mt-4">
                            <h2 class="text-xl font-bold mb-4">Заполните детали поиска</h2>
                        </div>

                        <form @submit.prevent="searchDossiers()">
                            <div class="grid grid-cols-3 gap-4">
                                <div class="col">
                                    <div class="form-group">
                                        <label class="block text-sm font-medium leading-6 text-gray-900">Фамилия клиента</label>
                                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1.5" v-model="dossier.contract.client.last_name">
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-group">
                                        <label class="block text-sm font-medium leading-6 text-gray-900">Имя клиента</label>
                                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1.5" v-model="dossier.contract.client.name">
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-group">
                                        <label class="block text-sm font-medium leading-6 text-gray-900">Отчество клиента</label>
                                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1.5" v-model="dossier.contract.client.middle_name">
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-group">
                                        <label class="block text-sm font-medium leading-6 text-gray-900">Паспорт клиента</label>
                                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1.5" v-model="dossier.contract.client.passport">
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-group">
                                        <label class="block text-sm font-medium leading-6 text-gray-900">Дата рождения</label>
                                        <input type="date" class="border border-gray-300 rounded-lg px-2 py-1.5" v-model="dossier.contract.client.birthday">
                                    </div>
                                </div>

                                <div class="col">
                                    <div class="form-group">
                                        <label class="block text-sm font-medium leading-6 text-gray-900">Продукт (выбрать)</label>
                                        <select class="border border-gray-300 rounded-lg px-2 py-1.5" v-model="dossier.contract.product.name">
                                            <option v-for="product in products" v-bind:value="product.name">{{product.name}}</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-group">
                                        <label class="block text-sm font-medium leading-6 text-gray-900">Номер договора</label>
                                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1.5" v-model="dossier.contract.contract_number">
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-group">
                                        <label class="block text-sm font-medium leading-6 text-gray-900">Штрих-код досье</label>
                                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1.5" v-model="dossier.barcode">
                                    </div>
                                </div>
                            </div>
                            <div class="mt-4">
                                <button type="submit" class="mr-4 rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500">
                                    Поиск
                                </button>
                                <span class="danger">{{ errArray['detail'] ? errArray['detail'].toString() : '' }}</span>
                                <span id="err" class="danger"></span>
                            </div>

                        </form>
                    </div>

                    <!-- Search Result -->
                    <div v-if="Object(foundDossiers).length!==0" class="mt-5">
                        <div class="flex items-center">
                            <button @click="foundDossiers=[]" class="rounded-md bg-purple-600 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-purple-500">
                                Назад
                            </button>
                            <h1 class="text-2xl font-bold ml-4">Результаты поиска</h1>
                        </div>
                        <div class="p-1 bg-white rounded-lg mt-5">

                            <div class="grid grid-cols-4 mb-3">
                                <div class="col"><b>Клиент</b></div>
                                <div class="col"><b>Продукт:</b></div>
                                <div class="col"><b>Номер договора:</b></div>
                                <div class="col"><b></b></div>
                            </div>

                            <div v-for="dossier in foundDossiers" :key="dossier.id" class="highlighted">
                                <ul>
                                    <details>
                                        <summary>
                                            <div class="grid grid-cols-4">
                                                <div class="col">{{ dossier.contract.client.last_name }} {{ dossier.contract.client.first_name }} {{ dossier.contract.client.middle_name }}</div>
                                                <div class="col">{{ dossier.contract.product.name }}</div>
                                                <div class="col">{{ dossier.contract.contract_number }}</div>
                                                <div class="col">
                                                    <button @click="addRemoveDossierToRequest(dossier)" 
                                                    class="rounded-md px-2 py-0.2 text-sm font-semibold text-white shadow-sm "
                                                    :class="{ 
                                                    'bg-gray-500 hover:bg-gray-600': addedDossiers.includes(dossier), 
                                                    'bg-green-500 hover:bg-green-600': !addedDossiers.includes(dossier) }">
                                                        Добавить/убрать
                                                    </button>
                                                </div>
                                            </div>
                                        </summary>
                                        <div class="mt-3 text-sm">
                                            <li><b>Дата рождения:</b>     {{ dossier.contract.client.birthday }}</li>
                                            <li><b>Паспорт:</b>     {{ dossier.contract.client.passport}}</li>
                                            <li><b>Штрих-код досье:</b>     {{ dossier.barcode }}</li>
                                        </div>
                                    </details>
                                </ul>
                            </div> 
                        </div>
                    </div>
                </div>
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

        data() {
            return {
                currentRequest:{},
                showSearch: false,
                showDialog: false,
                foundDossiers:[],
                addedDossiers:[],
                emptyResult: false,
                errArray: [],
                products:[
                  {name:''},
                  {name:'ДБО'},
                  {name:'Кредит'},
                  {name:'Кредитная карта'},
                  {name:'Вклад'},
                  {name:'Дебетовая карта'}

              ],
                dossier:{
                    'id':'',
                    'barcode':'',
                    'status':'',
                    'contract':{
                        'id':'',
                        'contract_number':'',
                        'time_create':'',
                        'client':{
                            'id':'',
                            'last_name':'',
                            'name':'',
                            'middle_name':'',
                            'passport':'',
                            'birthday':'',
                        },
                        'product':{
                            'id':'',
                            'name':''
                        }
                    },
                },
            }
        },

        mounted() {
            this.getRequest();
        },
    
        methods: {
            getRequest(){
                axios.get('/api/requests/requests/' + this.$route.params.id + '/',
                            ).then(response =>{
                                    console.log(response.data)
                                    this.currentRequest = response.data
                                    this.addedDossiers = response.data.dossiers
                                    }         
                        ).catch(error =>{
                            console.log(error)
                        })
            },
            searchDossiers(){
                axios.get('/api/units/dossier/' + 
                    '?barcode='+ this.dossier.barcode +
                    '&contract__contract_number='+this.dossier.contract.contract_number +
                    '&contract__client__last_name='+this.dossier.contract.client.last_name +
                    '&contract__client__first_name='+this.dossier.contract.client.name +
                    '&contract__client__middle_name='+this.dossier.contract.client.middle_name +
                    '&contract__client__passport='+this.dossier.contract.client.passport + 
                    '&contract__client__birthday='+this.dossier.contract.client.birthday +
                    '&contract__product__name='+this.dossier.contract.product.name + 
                    '&limit=10',
                    ).then(response =>{
                            console.log(response.data);
                            this.foundDossiers = response.data;
                            this.errArray = [];
                            }                              
                ).catch(error =>{
                    if (error.response) {
                        console.log(error.response.data);
                        this.errArray = error.response.data;
                }
                }
                )
            },

            addRemoveDossierToRequest(dossier){
                const index = this.addedDossiers.indexOf(dossier);

                if (index !== -1) {
                    this.addedDossiers.splice(index, 1);
                } else {
                    this.addedDossiers.push(dossier);
                }
            },
            
            requestSend(){
                if(this.addedDossiers.length !==0 && this.currentRequest.status == 'creation'){
                this.currentRequest.dossiers = this.getID(this.addedDossiers)
                this.currentRequest.status = 'sent_for_processing'
                this.currentRequest.time_create = this.getCurrentDateTime()
                axios.patch('/api/requests/requests/'+ this.currentRequest.id + '/', this.currentRequest
                            ).then(response =>{
                                    console.log(response.data)
                                    this.$router.push({
                                        name:'myRequests'
                                    })
                                    }         
                        ).catch(error =>{
                            console.log(error)
                            this.currentRequest.status = 'creation'
                        }
                        )
                }         
            },
            createTasks() {
                let tasks = []
                for (let i = 0; i < this.addedDossiers.length; i++ ){
                    let dossier = this.addedDossiers[i];
                    let task = {
                                dossier:dossier.barcode,
                                request:this.currentRequest.id,
                                task_status:"accepted"
                                }
                    tasks.push(task)
                }
                axios.post('/api/requests/tasks/', tasks
                    ).then(response =>{
                        console.log(response.data)
                        this.$router.push({
                                        name:'requestList'
                                    });
                    }
                ).catch(error =>{
                    console.log(error)
                });
            
            },

            requestAccept(){
                if(this.currentRequest.status == 'sent_for_processing'){
                axios.patch('/api/requests/requests/'+ this.currentRequest.id + '/', {status:'accepted'}
                            ).then(response =>{
                                    console.log(response.data);
                                    this.createTasks();
                                    }         
                        ).catch(error =>{
                            console.log(error)
                            this.currentRequest.status = 'sent_for_processing'
                        }
                        )
                }         
            },
            requestCancel(){
                if(this.currentRequest.status !== 'creation'){
                axios.patch('/api/requests/requests/'+ this.currentRequest.id + '/',
                        {
                        status:'cancelled',
                        close_reason:this.currentRequest.close_reason,
                        closer:this.userStore.user.id
                        }
                            ).then(response =>{
                                    console.log(response.data)
                                    this.$router.push({
                                        name:'requestList'
                                    })
                                    }         
                        ).catch(error =>{
                            console.log(error)
                        }
                    )
                }
            },

            requestDelete(){
                if(this.currentRequest.status == 'creation'){
                axios.delete('/api/requests/requests/'+ this.currentRequest.id + '/',
                            ).then(response =>{
                                    console.log(response.data)
                                    this.$router.push({
                                        name:'myRequests'
                                    })
                                    }         
                        ).catch(error =>{
                            console.log(error)
                        }
                        )
                }
            },

            getID(objectsArray){
                let idArray = []
                for (let i = 0; i < objectsArray.length; i++) {
                    idArray.push(objectsArray[i].barcode);
                    }
                return idArray
            },

            getCurrentDateTime() {
                const currentDate = new Date();
                const formattedDate = currentDate.toISOString().slice(0, 19);
                return formattedDate;
            },
            
            hasGroup(groupName) {
            return this.userStore.user && this.userStore.user.groups.some(group => group.name === groupName);
            },
        }
    }
    </script>