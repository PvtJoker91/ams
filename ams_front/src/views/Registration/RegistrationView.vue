<template>
    <div class="space-y-3">
        <h2 class="text-3xl font-bold mb-4">Регистрация</h2>
        <div class="p-6 bg-white border border-gray-200 rounded-lg">
            <div class="p-1 bg-white  rounded-lg">
                <div>
                    <form @submit.prevent="openArchiveBox()" class="flex items-center">
                        <label class="mr-2">Открыть архивный бокс:</label>
                        <input type="text" v-model="archiveBox.barcode" class="border border-gray-300 rounded-lg px-2 py-1 mr-4">
                        <span class="danger">{{ errArray['detail'] ? errArray['detail'].toString() : '' }}</span>
                        <span class="danger">{{errArray['non_field_errors'] ? errArray['non_field_errors'].toString() : ''}}</span>
                        <span id="err" class="danger"></span>
                    </form>
                </div>

                <div v-if="Object.keys(this.currentArchiveBox).length !== 0" class="mt-2">
                    <button class="py-1 px-2 bg-purple-600 text-white rounded-lg shadow-sm hover:bg-purple-500" @click="closeArchiveBox()">Закрыть бокс</button>
                </div>
            </div>

            <div class="p-1 bg-white  rounded-lg" v-if="Object.keys(this.currentArchiveBox).length !== 0">
                <form id="dossierBarcodeForm" @submit.prevent="saveDossier" class="flex items-center">
                    <label class="form-label mr-2">Введите ш/к для регистрации досье:</label>
                    <input type="text" class="border border-gray-300 rounded-lg px-2 py-1" v-model="dossier.barcode">
                    <span class="danger">{{errArray['validation_error'] ? errArray['validation_error'].toString() : ''}}</span>
                    <span class="danger">{{errArray['dossier_status_error'] ? errArray['dossier_status_error'].toString() : ''}}</span>
                    <span class="danger">{{errArray['dossier_box_error'] ? errArray['dossier_box_error'].toString() : ''}}</span>
                    <span id="err" class="danger"></span>
                </form>
            </div>
        </div>
        <div class="p-6 bg-white border border-gray-200 rounded-lg" v-if="Object.keys(this.currentDossier).length !== 0 && Object.keys(this.currentContract).length === 0 && Object.keys(this.contracts).length === 0">
            <h2 class="text-2xl font-bold mb-4">Поиск договоров клиентов</h2>
            <form @submit.prevent="searchContract" class="mb-4">
                <div class="grid grid-cols-1 gap-4">
                    <div>
                        <label class="mr-2">Фамилия</label>
                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1" v-model="contract.client__last_name">
                    </div>

                    <div>
                        <label class="mr-2">Имя</label>
                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1" v-model="contract.client__first_name">
                    </div>

                    <div>
                        <label class="mr-2">Отчество</label>
                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1" v-model="contract.client__middle_name">
                    </div>

                    <div>
                        <label class="mr-2">Паспорт</label>
                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1" v-model="contract.client__passport">
                    </div>

                    <div>
                        <label class="mr-2">Номер договора</label>
                        <input type="text" class="border border-gray-300 rounded-lg px-2 py-1" v-model="contract.contract_number">
                    </div>
                </div>

                <div class="mt-4">
                    <button type="submit" class="py-1 px-2 bg-purple-600 text-white rounded-lg shadow-sm hover:bg-purple-500">Поиск</button>
                </div>
                <span class="danger">{{errArray['to_many'] ? errArray['to_many'].toString() : ''}}</span>
                <span id="err" class="danger"></span>
            </form>
        </div>

        <div class="p-3 bg-white border border-gray-200 rounded-lg" v-if="Object(this.contracts).length !==0" >
            <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        N
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Продукт
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Номер договора
                    </th>
                    <th scope="col" class="px-6 py-3">
                        ФИО
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Дата рождения
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Паспорт
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="contract, n in makePage()" :key="contract.id" @click="saveContract(contract)" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <th scope="row" class="px-6 py-1 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{n + (currentPage-1)*10 + 1}}
                    </th>
                    <td class="px-6 py-1">
                        {{ contract.product.name }}
                    </td>
                    <td class="px-6 py-1">
                        {{ contract.contract_number }}
                    </td>
                    <td class="px-6 py-1">
                        {{ contract.client.last_name }} {{ contract.client.first_name }} {{ contract.client.middle_name }}
                    </td>
                    <td class="px-6 py-1">
                        {{ contract.client.birthday }}
                    </td>
                    <td class="px-6 py-1">
                        {{ contract.client.passport }}
                    </td>
                </tr>
            </tbody>
        </table>
        <nav class="flex items-center flex-column flex-wrap md:flex-row justify-between pt-4" aria-label="Table navigation">
            <span class="text-sm font-normal text-gray-500 dark:text-gray-400 ml-3 mb-3 md:mb-0 block w-full md:inline md:w-auto">
                Показано 
              <span class="font-semibold text-gray-900 dark:text-white">{{showingElems()}}</span> из 
              <span class="font-semibold text-gray-900 dark:text-white">{{contracts.length}}</span>
            </span>
            <ul class="inline-flex -space-x-px rtl:space-x-reverse text-sm h-8 mr-3 mb-3">
                <li v-if="currentPage>1">
                    <button  @click="loadPreviousPage" class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Previous</button>
                </li>
                <li v-if="currentPage>3">
                    <button  @click="loadRequestedPage(1)" class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">1</button>
                </li>
            
                <li v-if="totalPages()>1" v-for="index in generatePagesRange(currentPage, totalPages(), 2)">
                    <button  @click="loadRequestedPage(index + 1)" 
                    :class="{
                      'flex items-center justify-center px-3 h-8 text-blue-600 border border-gray-300 bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white'
                      :index+1==currentPage,
                      'flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white'
                      :index+1!==currentPage}">
                    {{index + 1}}</button>
                </li>
                <li v-if="currentPage<totalPages()-2">
                    <button  @click="loadRequestedPage(totalPages())" class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">{{totalPages()}}</button>
                </li>
                <li v-if="currentPage<totalPages()">
                    <button  @click="loadNextPage" class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Next</button>
                </li>
            </ul>
        </nav>

        </div>

        <div class="p-12 bg-white border border-gray-200 rounded-lg" v-if="Object.keys(this.currentContract).length !== 0">
            <div class="container mx-auto grid grid-cols-3 gap-4">
                <div>
                    <b class="block">Клиент: </b>
                    <span class="block">{{ currentContract.client.last_name }} {{ currentContract.client.first_name }} {{ currentContract.client.middle_name }}</span>
                </div>
                <div>
                    <b class="block">Дата рождения: </b>
                    <span class="block">{{ currentContract.client.birthday }}</span>
                </div>
                <div>
                    <b class="block">Номер паспорта: </b>
                    <span class="block">{{ currentContract.client.passport }}</span>
                </div>
                <div>
                    <b class="block">Продукт: </b>
                    <span class="block">{{ currentContract.product.name }}</span>
                </div>
                <div>
                    <b class="block">Номер договора: </b>
                    <span class="block">{{ currentContract.contract_number }}</span>
                </div>
                <div>
                    <b class="block">Дата заключения: </b>
                    <span class="block">{{ currentContract.time_create }}</span>
                </div>
            </div>         
            <div class="mt-4">
                <button class="py-1 px-2 bg-purple-600 text-white rounded-lg shadow-sm hover:bg-purple-500" @click="registerDossier()">Зарегистрировать</button>
            </div>
        </div>

        <div class="p-2 bg-white border border-gray-200 rounded-lg" v-if="Object.keys(dossiers).length !== 0">
            <h5 class="text-xl font-bold mb-4">Зарегистрированные досье в AB: ({{dossiers.length}})</h5>
            <ul>
                <li v-for="dossier in dossiers" class="mb-1">
                    {{ dossier.barcode }}
                </li>
            </ul>
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
        currentArchiveBox: {},
        currentDossier: {},
        currentContract: {},
        dossiers:[],
        contracts:[],
        currentPage: 1,
        errArray: [],
        'archiveBox': {
            'barcode':'',
            'status':'Under registration',
            'current_sector':'1',
            "storage_address":"",
        },
        'dossier':{
            'barcode':'',
            'archive_box':'',
            'contract':'',
            'current_sector':'1',
            'status':'',
        },
        'contract':{
            'id':'',
            'contract_number':'',
            'client__last_name':'',
            'client__first_name':'',
            'client__middle_name':'',
            'client__passport':'',
        },
        }
    },

    methods: {

    openArchiveBox(){
        if (this.archiveBox.barcode) {
            axios.post('/api/registration/ab/', this.archiveBox).then(
            response =>{
                console.log(response.data)
                this.currentArchiveBox = response.data
                this.dossiers = response.data.dossiers
                this.errArray = []
                this.contracts = []
                this.currentDossier = {}
                this.currentContract = {}
            }
        ).catch(error =>{
            if (error.response) {
      console.log(error.response.data);
      this.errArray = error.response.data;
      this.currentArchiveBox = {};
      this.dossiers = [];

    }
    })

    }
    },

    closeArchiveBox(){
        if (this.dossiers.length == 0){
        axios.delete('/api/registration/ab/' + this.currentArchiveBox.barcode + '/').then(
            response =>{
                console.log(response.data)
                this.currentArchiveBox = {}
                this.contracts = []
                this.currentDossier = {}
                this.currentContract = {}
            }
        ).catch(error =>{
            console.log(error)
        })
  
      } else {
        this.currentArchiveBox.status = 'Is registered'
        axios.post('/api/registration/ab/', this.currentArchiveBox).then(
            response =>{
                console.log(response.data)
                this.dossiers = []
                this.currentArchiveBox = {}
                this.contracts = []
                this.currentDossier = {}
                this.currentContract = {}
            }
        ).catch(error =>{
            console.log(error)
        })
    }
    },


    saveDossier(){
        axios.get('/api/registration/dossier/'+ '?barcode=' + this.dossier.barcode).then(
            response =>{
                console.log(response.data)
                if (response.data.length == 0){
                this.currentDossier = this.dossier;
                this.contracts = [];
                this.currentContract = {};
                this.errArray = [];
            } else {this.currentDossier = {}} 
            }
        ).catch(error =>{
            if (error.response) {
                console.log(error.response.data);
                this.errArray = error.response.data;

                }
        })
    },

    searchContract(){
        this.currentPage = 1;
        axios.get('/api/contracts/' + 
                    '?contract_number='+this.contract.contract_number +
                    '&client__last_name='+this.contract.client__last_name +
                    '&client__first_name='+this.contract.client__first_name +
                    '&client__middle_name='+this.contract.client__middle_name +
                    '&client__passport='+this.contract.client__passport + 
                    '&limit=100',
                    ).then(response =>{
                            console.log(response.data);
                            this.contracts = response.data;
                            this.errArray = [];
                            if (this.contracts.length == 1){
                                this.saveContract(this.contracts[0]);
                            }                         
                            }          
                ).catch(error =>{
                    if (error.response) {
                        console.log(error.response.data);
                        this.errArray = error.response.data;
                }
                }
                )
    },

    saveContract(contract){
        this.currentContract = contract
        this.currentDossier.contract = this.currentContract.id
        this.contracts = []    
        },
  
    registerDossier(){
        this.currentDossier.status = 'Is registred';
        this.currentDossier.archive_box = this.currentArchiveBox.id;
        this.currentDossier.registerer = this.userStore.user.id;
        axios.post('/api/registration/dossier/', this.currentDossier).then(
            response =>{
                console.log(response.data)
                if(response.data){
                    this.dossiers.push(response.data);
                    this.contracts = [];
                    this.currentDossier = {};
                    this.currentContract = {};
                    this.dossier.barcode = '';
                    this.contract.contract_number = '';
                    this.contract.client__last_name = '';
                    this.contract.client__first_name = '';
                    this.contract.client__middle_name = '';
                    this.contract.client__passport = '';
                }              
            }
        ).catch(error =>{
            console.log(error)
        })
    },

    totalPages(){
        if (this.contracts.length % 10 == 0){
          return Math.floor(this.contracts.length / 10)
        } else {
          return Math.floor(this.contracts.length / 10) + 1
        };
    },

    makePage(){
        let start = (this.currentPage - 1) * 10;
        let end = this.currentPage * 10;
        return this.contracts.slice(start, end)
    },

    loadNextPage() {
        this.currentPage = this.currentPage + 1;
        this.makePage();
    },
    loadPreviousPage() {
        this.currentPage = this.currentPage - 1;
        this.makePage();
    },

    loadRequestedPage(page) {
        this.currentPage = page;
        this.makePage();
    },
    generatePagesRange(currentPage, totalPages, gap) {
        const range = [];
        let start = Math.max(0, currentPage - gap - 1);
        let end = Math.min(currentPage + gap, totalPages);
        for (let i = start; i <= end - 1; i++) {
            range.push(i);
        }
        return range;
    },

    showingElems(){
        if (this.contracts.length!=0){ 
        let start = (this.currentPage - 1)*10 + 1;
        let end = Math.min(this.currentPage*10, this.contracts.length);
        return `${start} - ${end}`}
        else return 0
    },
    


    }

}
</script>