<template>
  <div v-if="userStore.user.isAuthenticated && userStore.user.id">
    <h2 class="text-3xl font-bold mb-8">Реестры</h2>
        <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
          <div class="flex flex-column ">
            <div class="mr-3 mb-3">
                <button id="dropdownRegistryTypeButton" @click="toggleRegistryType = !toggleRegistryType" class="inline-flex items-center text-gray-500 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-3 py-1.5 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700" type="button">
                    Тип {{ filteredRegistryType }}
                    <svg class="w-2.5 h-2.5 ms-2.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
                    </svg>
                </button>
                <!-- Dropdown menu -->
                <div v-if="toggleRegistryType" id="dropdownRegistryType" class="z-10 w-48 bg-white divide-y divide-gray-100 rounded-lg shadow dark:bg-gray-700 dark:divide-gray-600" style="position: absolute;  margin: 0px; ">
                    <ul class="p-3 space-y-1 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownRegistryTypeButton">
                        <li >
                            <div class="flex items-center p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600">
                                <input v-model="filteredRegistryType"  id="filter-radio-example-1" type="radio" value="lr" name="filter-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                                <label for="filter-radio-example-1" class="w-full ms-2 text-sm font-medium text-gray-900 rounded dark:text-gray-300">LR</label>
                            </div>
                        </li>
                        <li>
                          <div class="flex items-center p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600">
                              <input v-model="filteredRegistryType"  id="filter-radio-example-2" type="radio" value="rl" name="filter-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                              <label for="filter-radio-example-2" class="w-full ms-2 text-sm font-medium text-gray-900 rounded dark:text-gray-300">RL</label>
                          </div>
                      </li>
                      <li>
                          <div class="flex items-center p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600">
                              <input v-model="filteredRegistryType"  id="filter-radio-example-3" type="radio" value="rc" name="filter-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                              <label for="filter-radio-example-3" class="w-full ms-2 text-sm font-medium text-gray-900 rounded dark:text-gray-300">RC</label>
                          </div>
                      </li>      
                    </ul>
                </div>
            </div>
            <div class="mr-3 mb-3">
                <button id="dropdownRegistryStatusButton" @click="toggleRegistryStatus = !toggleRegistryStatus" class="inline-flex items-center text-gray-500 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-3 py-1.5 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700" type="button">
                    Статус {{ filteredRegistryStatus }}
                    <svg class="w-2.5 h-2.5 ms-2.5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
                    </svg>
                </button>
                <!-- Dropdown menu -->
                <div v-if="toggleRegistryStatus" id="dropdownRegistryStatus" class="z-10 w-48 bg-white divide-y divide-gray-100 rounded-lg shadow dark:bg-gray-700 dark:divide-gray-600" style="position: absolute;  margin: 0px; ">
                    <ul class="p-3 space-y-1 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownRegistryStatusButton">
                        <li >
                            <div class="flex items-center p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600">
                                <input v-model="filteredRegistryStatus"  id="filter-radio-example-1" type="radio" value="creation" name="filter-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                                <label for="filter-radio-example-1" class="w-full ms-2 text-sm font-medium text-gray-900 rounded dark:text-gray-300">Creation</label>
                            </div>
                        </li>
                        <li>
                          <div class="flex items-center p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600">
                              <input v-model="filteredRegistryStatus"  id="filter-radio-example-2" type="radio" value="sent" name="filter-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                              <label for="filter-radio-example-2" class="w-full ms-2 text-sm font-medium text-gray-900 rounded dark:text-gray-300">Sent</label>
                          </div>
                      </li>
                      <li>
                          <div class="flex items-center p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600">
                              <input v-model="filteredRegistryStatus"  id="filter-radio-example-3" type="radio" value="on_acceptance" name="filter-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                              <label for="filter-radio-example-3" class="w-full ms-2 text-sm font-medium text-gray-900 rounded dark:text-gray-300">On acceptance</label>
                          </div>
                      </li>
                      <li>
                          <div class="flex items-center p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-600">
                              <input v-model="filteredRegistryStatus"  id="filter-radio-example-4" type="radio" value="accepted" name="filter-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                              <label for="filter-radio-example-4" class="w-full ms-2 text-sm font-medium text-gray-900 rounded dark:text-gray-300">Accepted</label>
                          </div>
                      </li>    
                    </ul>
                </div>
            </div>
            <div class="mr-0">
                <button @click="clearFilters" class="inline-flex items-center text-gray-500 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-3 py-1.5 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700" type="button">
                    Очистить фильтры
                </button>
            </div>
          </div>
        
          <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                      Номер
                    </th>
                    <th scope="col" class="px-6 py-3">
                      Тип
                    </th>
 
                    <th scope="col" class="px-6 py-3">
                        <div class="flex items-center">
                            Дата создания
                            <button @click="addOrdering('ordering=time_create')"><svg class="w-3 h-3 ms-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M8.574 11.024h6.852a2.075 2.075 0 0 0 1.847-1.086 1.9 1.9 0 0 0-.11-1.986L13.736 2.9a2.122 2.122 0 0 0-3.472 0L6.837 7.952a1.9 1.9 0 0 0-.11 1.986 2.074 2.074 0 0 0 1.847 1.086Zm6.852 1.952H8.574a2.072 2.072 0 0 0-1.847 1.087 1.9 1.9 0 0 0 .11 1.985l3.426 5.05a2.123 2.123 0 0 0 3.472 0l3.427-5.05a1.9 1.9 0 0 0 .11-1.985 2.074 2.074 0 0 0-1.846-1.087Z"/>
                          </svg></button>
                        </div>
                    </th>
                    <th scope="col" class="px-6 py-3">
                            Количество досье
                    </th>
                    <th scope="col" class="px-6 py-3">
                        <div class="flex items-center">
                            Статус
                            <button @click="addOrdering('ordering=status')"><svg class="w-3 h-3 ms-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M8.574 11.024h6.852a2.075 2.075 0 0 0 1.847-1.086 1.9 1.9 0 0 0-.11-1.986L13.736 2.9a2.122 2.122 0 0 0-3.472 0L6.837 7.952a1.9 1.9 0 0 0-.11 1.986 2.074 2.074 0 0 0 1.847 1.086Zm6.852 1.952H8.574a2.072 2.072 0 0 0-1.847 1.087 1.9 1.9 0 0 0 .11 1.985l3.426 5.05a2.123 2.123 0 0 0 3.472 0l3.427-5.05a1.9 1.9 0 0 0 .11-1.985 2.074 2.074 0 0 0-1.846-1.087Z"/>
                          </svg></button>
                        </div>
                    </th>
                    <th scope="col" class="px-6 py-3">
                        <span class="sr-only">Детали</span>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="registry in elements" :key="registry.id" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <th scope="row" class="px-6 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                      <RouterLink :to="{name: 'registryDetail', params:{'id': registry.id}}" target="_blank" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">
                        {{ registry.id }}
                      </RouterLink>
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
                      {{ registry.status }}
                    </td>
                    <td>
                    <button v-if="registry.status=='creation'"
                      @click="sendRegistry(registry)" class="rounded-md bg-indigo-600 px-3 py-2 text-xs font-semibold text-white shadow-sm hover:bg-indigo-500">
                        Отправить
                      </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <nav class="flex items-center flex-column flex-wrap md:flex-row justify-between pt-4" aria-label="Table navigation">
            <span class="text-sm font-normal text-gray-500 dark:text-gray-400 ml-3 mb-3 md:mb-0 block w-full md:inline md:w-auto">
                Показано 
              <span class="font-semibold text-gray-900 dark:text-white">{{showingElems()}}</span> из 
              <span class="font-semibold text-gray-900 dark:text-white">{{paginationInfo.totatElements}}</span>
            </span>
            <ul class="inline-flex -space-x-px rtl:space-x-reverse text-sm h-8 mr-3 mb-3">
                <li v-if="paginationInfo.currentPage>1">
                    <button  @click="loadPreviousPage" class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Previous</button>
                </li>
                <li v-if="paginationInfo.currentPage>3">
                    <button  @click="loadRequestedPage(1)" class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">1</button>
                </li>
            
                <li v-if="paginationInfo.totalPages>1" v-for="index in generatePagesRange(paginationInfo.currentPage, paginationInfo.totalPages, 2)">
                    <button  @click="loadRequestedPage(index + 1)" 
                    :class="{
                      'flex items-center justify-center px-3 h-8 text-blue-600 border border-gray-300 bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white'
                      :index+1==paginationInfo.currentPage,
                      'flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white'
                      :index+1!==paginationInfo.currentPage}">
                    {{index + 1}}</button>
                </li>
                <li v-if="paginationInfo.currentPage<paginationInfo.totalPages-2">
                    <button  @click="loadRequestedPage(paginationInfo.totalPages)" class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">{{paginationInfo.totalPages}}</button>
                </li>
                <li v-if="paginationInfo.currentPage<paginationInfo.totalPages">
                    <button  @click="loadNextPage" class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Next</button>
                </li>
            </ul>
        </nav>
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
          elements: [],
          pageUrl: '/api/units/registry/?',
          cleanUrl: '/api/units/registry/?',
          paginationInfo: {
            currentPage:null,
            totatElements:null,
            totalPages:null,
          },
          params:'',
          ordering:'',
          toggleRegistryType: false,
          filteredRegistryType: '',
          toggleRegistryStatus: false,
          filteredRegistryStatus: '',
          }
          
      },
      mounted() {
        this.loadElements();
      },

      watch: {
        filteredRegistryType: {
          handler() {
            this.toggleRegistryType = false,
            this.changeParams(`type=${this.filteredRegistryType}&`)
          },
        },
        filteredRegistryStatus: {
          handler() {
            this.toggleRegistryStatus = false,
            this.changeParams(`status=${this.filteredRegistryStatus}&`)
          },
        },
      },
    
      methods: {
        sendRegistry(registry){
          registry.status = 'sent';
          registry.sender = this.userStore.user.id
          axios.patch('/api/units/registry/' + registry.id + '/', registry).then(
              response =>{
                  console.log(response.data);
              }
          ).catch(error =>{
              if (error.response) {
                  console.log(error.response.data);
                  this.errArray = error.response.data;
                  }
              })
        },

        addOrdering(newOrdering){
          if (this.ordering == newOrdering){
            let paramName = newOrdering.slice(newOrdering.indexOf("=") + 1,);
            this.ordering = this.ordering.slice(0, this.ordering.indexOf("=") + 1) + "-" + paramName;
          } else {
            this.ordering = newOrdering
          };
          this.pageUrl = this.cleanUrl + this.params + this.ordering ;
          this.loadElements();
        },

        changeParams(param) {
          let paramName = param.slice(0, param.indexOf("=") + 1);
          if (!this.params.includes(paramName)) {
            this.params = this.params + param;
          } else {
            this.params = this.params.replace(new RegExp(paramName + "[^&]*" + "&"), param );
          };
          this.pageUrl = this.cleanUrl + this.params;
          this.loadElements();
        },

        loadElements(){
          axios.get(this.pageUrl).then(
            response =>{
              console.log(response.data)
              this.elements = response.data.results;
              this.paginationInfo = {
                currentPage: response.data.current_page,
                totalPages: response.data.pages,
                totatElements: response.data.count
              };
              this.pageUrl = response.data.next;
              } 
              ).catch(error =>{
                    if (error.response) {
                      console.log(error.response.data)
                    }
                    })
        },

        clearFilters(){
          this.params = '';
          this.ordering = '';
          this.filteredRegistryType = '',
          this.filteredRegistryStatus = '',
          this.pageUrl = this.cleanUrl;
          this.loadElements();
        },


        loadNextPage() {
          const nextPage = parseInt(this.paginationInfo.currentPage) + 1;
          this.pageUrl = this.cleanUrl + "page=" + nextPage + "&" + this.params + this.ordering;
          this.loadElements();
        },
        loadPreviousPage() {
          const previousPage = parseInt(this.paginationInfo.currentPage) - 1;
          this.pageUrl = this.cleanUrl + "page=" + previousPage + "&" + this.params + this.ordering;
          this.loadElements();
        },
    
        loadRequestedPage(page) {
          this.pageUrl = this.cleanUrl + "page=" + page + "&" + this.params + this.ordering;
          this.loadElements();
      
        },
        generatePagesRange(currentPage, totalPages, gap) {
          const range = [];
          currentPage = parseInt(currentPage)
          let start = Math.max(0, currentPage - gap - 1);
          let end = Math.min(currentPage + gap, totalPages);
          for (let i = start; i <= end - 1; i++) {
            range.push(i);
          }
          return range;
        },

        showingElems(){
          if (this.paginationInfo.totatElements){ 
          let start = (this.paginationInfo.currentPage - 1)*10 + 1;
          let end = Math.min(this.paginationInfo.currentPage*10, this.paginationInfo.totatElements);
          return `${start} - ${end}`}
          else return 0
        },
      }
    
    }
    </script> 
    
      