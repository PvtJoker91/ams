<template>
  <div v-if="userStore.user.isAuthenticated && userStore.user.id">
  <div v-if="!showCard" class="bg-white border border-gray-200 rounded-lg flex items-center justify-center h-80">
      <form @submit.prevent="unitSearch">
          <label class="block mb-2 text-xl font-bold">Для просмотра информации о единице хранения</label><br>
          <label>Введите штрих-код досье или архивного бокса</label><br>
          <input type="text" v-model="barcode" placeholder="Штрих-код ЕХ" class="w-full mt-10 py-2 px-6 border border-gray-200 rounded-lg">
          <span class="danger">{{ errArray['non_field_errors'] ? errArray['non_field_errors'].toString() : '' }}</span>
          <span class="danger">{{ errArray['detail'] ? errArray['detail'].toString() : '' }}</span>
          <span id="err" class="danger"></span>
      </form>
  </div>



  <div v-if="showCard">
    <div class="flex items-center">
      <button class="mb-6 mr-6 rounded-md bg-purple-600 px-1 py-1 text-sm font-semibold text-white shadow-sm hover:bg-purple-500" 
          @click="showCard=false">Назад
      </button>
      <h2 v-if="Object.keys(dossier).length!=0" class="text-2xl font-bold mb-8">Карточка досье {{dossier.barcode}}</h2>
      <h2 v-if="Object.keys(archive_box).length!=0" class="text-2xl font-bold mb-8">Карточка архивного бокса {{archive_box.barcode}}</h2>
    </div>

    <div class="p-8 bg-white rounded-lg">
      <div class="flex items-center">
          <button class="mr-4 mb-3 rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500" 
              @click="showHistory=false">Информация о EХ
          </button>
          <button class="mb-3 rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500" 
              @click="showHistory=true, currentPage=1">История EХ
          </button>
      </div>

      <div v-if="!showHistory" class="flex mt-3" >
          <div class="flex-1">
            <h2 class="text-xl font-bold mb-4">Информация о хранении:</h2>
              <div class="container mx-auto grid grid-cols-2 gap-4 mb-6 mt-2">
                  <div>
                      <b class="block">Статус: </b>
                      <span v-if="Object.keys(dossier).length!=0" class="block">{{ dossier.status }}</span>
                      <span v-if="Object.keys(archive_box).length!=0" class="block">{{ archive_box.status }}</span>
                  </div>
                  <div v-if="Object.keys(dossier).length!=0">
                      <b class="block">Архивный бокс: </b>
                      <span v-if="dossier.archive_box!=null" class="block">{{ dossier.archive_box.barcode }}</span>
                  </div>
                  <div>
                      <b class="block">Сектор: </b>
                      <span v-if="Object.keys(dossier).length!=0" class="block">{{ dossier.current_sector.name }}</span>
                      <span v-if="Object.keys(archive_box).length!=0" class="block">{{ archive_box.current_sector.name }}</span>
                  </div>
                  <div>
                      <b class="block">Размещение в хранилище: </b>
                      <span v-if="Object.keys(dossier).length!=0" class="block">{{ dossier.location}}</span>
                      <span v-if="Object.keys(archive_box).length!=0" class="block">{{ archive_box.location}}</span>
                  </div>
                  <div v-if="Object.keys(archive_box).length!=0">
                      <b class="block">Количество досье: </b>
                      <span class="block">{{ archive_box.dossier_count }}</span>
                  </div>
              </div>
              <h2 v-if="Object.keys(dossier).length!=0" class="text-xl font-bold mb-4">Информация о договоре:</h2>
              <div v-if="Object.keys(dossier).length!=0" class="container mx-auto grid grid-cols-2 gap-4 mb-6 mt-2">
                  <div>
                      <b class="block">ФИО клиента: </b>
                      <span class="block">{{ dossier.contract.client.last_name }} {{ dossier.contract.client.first_name }} {{ dossier.contract.client.middle_name }}</span>
                  </div>
                  <div>
                      <b class="block">Тип продукта: </b>
                      <span class="block">{{ dossier.contract.product.name }}</span>
                  </div>
                  <div>
                      <b class="block">Номер договора: </b>
                      <span class="block">{{ dossier.contract.contract_number }}</span>
                  </div>
                  <div>
                      <b class="block">Дата заключения: </b>
                      <span class="block">{{ dossier.contract.time_create }}</span>
                  </div>
              </div>
              <h2 v-if="Object.keys(dossier).length!=0" class="text-xl font-bold mb-4">Информация о регистрации:</h2>
              <div v-if="Object.keys(dossier).length!=0" class="container mx-auto grid grid-cols-2 gap-4 mb-6 mt-2">
                  <div>
                      <b class="block">Дата регистрации: </b>
                      <span class="block">{{ dossier.registration_date }}</span>
                  </div>
                  <div>
                      <b class="block">Регистратор: </b>
                      <span class="block">{{ dossier.registerer.first_name }} {{ dossier.registerer.last_name}}</span>
                  </div>
              </div>
          </div>
        </div>
        <div v-if="showHistory">
          <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        N
                    </th>

                    <th scope="col" class="px-6 py-3">
                        Дата
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Статус
                    </th>
                    <th v-if="Object.keys(dossier).length!=0" scope="col" class="px-6 py-3">
                        Архивный бокс
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Хранение
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Сотрудник
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="change, n in makePage()" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <th scope="row" class="px-6 py-2 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                      {{ n + (currentPage-1)*10 + 1 }}
                    </th>
                    <td class="px-6 py-2">
                      {{ change.timestamp }}
                    </td>
                    <td class="px-6 py-2">
                      {{change.status}}
                    </td>
                    <td v-if="Object.keys(dossier).length!=0" class="px-6 py-2">
                      {{ change.archive_box }}
                    </td>
                    <td class="px-6 py-2">
                      {{ change.location }}
                    </td>
                    <td class="px-6 py-2">
                      {{ change.user_last_name }} {{ change.user_first_name }}
                    </td>
                </tr>
            </tbody>
        </table>
        <nav class="flex items-center flex-column flex-wrap md:flex-row justify-between pt-4" aria-label="Table navigation">
            <span class="text-sm font-normal text-gray-500 dark:text-gray-400 ml-3 mb-3 md:mb-0 block w-full md:inline md:w-auto">
                Показано 
              <span class="font-semibold text-gray-900 dark:text-white">{{showingElems()}}</span> из 
              <span class="font-semibold text-gray-900 dark:text-white">{{history.length}}</span>
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
        showCard:false,
        showHistory: false,
        history:[],
        currentPage: 1,
        barcode:'',
        errArray:[],
        archive_box:{},
        dossier:{
          'contract':{
              'client':{},
              'product':{}
            },
          'archive_box':{
            'barcode':''
          },
          'registerer':{
            'last_name':'',
            'first_name':'',
          },
        },
      }
    },

    methods: {
      unitSearch(){
        const dossier_pattern = /D\d{2}-\d{2}-\d{8}$|d{5}-d{5}-d{5}-d{5}-d{5}$|d{25}$/;
        const ab_pattern = /AB-\d{2}-\d{6}$/;
        if (dossier_pattern.test(this.barcode)){
          axios.get('/api/units/dossier/' + this.barcode + '/',
                    ).then(response =>{
                            console.log(response.data)
                            this.dossier = response.data;
                            this.history = response.data.history;
                            this.showCard = true;
                            this.archive_box = {};
                            }         
                ).catch(error =>{
                    console.log(error)
                })
        } else if (ab_pattern.test(this.barcode)){
          axios.get('/api/units/archive-box/' + this.barcode + '/',
                    ).then(response =>{
                            console.log(response.data)
                            this.archive_box = response.data;
                            this.history = response.data.history;
                            this.showCard = true;
                            this.dossier = {};
                            }         
                ).catch(error =>{
                    console.log(error)
                })
        } else {
          console.log('Wrong barcode format')
        }

      },

      totalPages(){
        if (this.history.length % 10 == 0){
          return Math.floor(this.history.length / 10)
        } else {
          return Math.floor(this.history.length / 10) + 1
        };
      },

      makePage(){
        let start = (this.currentPage - 1) * 10;
        let end = this.currentPage * 10;
        return this.history.slice(start, end)
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
        if (this.history.length!=0){ 
        let start = (this.currentPage - 1)*10 + 1;
        let end = Math.min(this.currentPage*10, this.history.length);
        return `${start} - ${end}`}
        else return 0
      },
      
    }
    
  };
  
  </script>