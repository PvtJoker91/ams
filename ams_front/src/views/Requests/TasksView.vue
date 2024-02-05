<template>
  <h2 class="text-3xl font-bold mb-8">Задания по заявкам</h2>
      <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
      <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                  <th scope="col" class="px-6 py-3">
                    Заявка
                  </th>
                  <th scope="col" class="px-6 py-3">
                        <div class="flex items-center">
                          Услуга
                          <button @click="addOrdering('ordering=request__service')"><svg class="w-3 h-3 ms-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8.574 11.024h6.852a2.075 2.075 0 0 0 1.847-1.086 1.9 1.9 0 0 0-.11-1.986L13.736 2.9a2.122 2.122 0 0 0-3.472 0L6.837 7.952a1.9 1.9 0 0 0-.11 1.986 2.074 2.074 0 0 0 1.847 1.086Zm6.852 1.952H8.574a2.072 2.072 0 0 0-1.847 1.087 1.9 1.9 0 0 0 .11 1.985l3.426 5.05a2.123 2.123 0 0 0 3.472 0l3.427-5.05a1.9 1.9 0 0 0 .11-1.985 2.074 2.074 0 0 0-1.846-1.087Z"/>
                      </svg></button>
                      </div>
                  </th>
                  <th scope="col" class="px-6 py-3">
                          Досье
                  </th>
                  <th scope="col" class="px-6 py-3">
                    Дата исполнения
                  </th>
                  <th scope="col" class="px-6 py-3">
                      <div class="flex items-center">
                        Статус
                          <button @click="addOrdering('ordering=task_status')"><svg class="w-3 h-3 ms-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
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
              <tr v-for="task in elements" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                  <th scope="row" class="px-6 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    {{ task.request.id }}
                  </th>
                  <td class="px-6 py-3">
                    {{ task.request.service }}
                  </td>
                  <td class="px-6 py-3">
                    {{ task.dossier }}
                  </td>
                  <td class="px-6 py-3">
                    {{ task.deadline }}
                  </td>
                  <td class="px-6 py-3">
                    {{ task.task_status }}
                  </td>
                  <td class="px-6 py-3 text-right">
                  <RouterLink :to="{name: 'requestDetail', params:{'id': task.request.id}}" target="_blank" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">
                    Детали
                  </RouterLink>
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
          elements: [],
          pageUrl: '/api/requests/tasks/?',
          cleanUrl: '/api/requests/tasks/?',
          paginationInfo: {
            currentPage:null,
            totatElements:null,
            totalPages:null,
          },
          params:'',
          ordering:'',
          }
          
      },
      mounted() {
        this.loadElements();
      },

  
    methods: {
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
  
    