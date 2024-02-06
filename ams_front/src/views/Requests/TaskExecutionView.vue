<template>
  <div v-if="userStore.user.isAuthenticated && userStore.user.id" class="space-y-3">
    <h2 class="text-3xl font-bold mb-4">Исполнить задание</h2>

      <div class="p-6 bg-white border border-gray-200 rounded-lg">
          <div class="p-1 bg-white  rounded-lg">
              <form @submit.prevent="findDossierTasks()" class="flex items-center">
                  <label class="form-label mr-2">Введите ш/к досье:</label>
                  <input type="text" class="form-control border border-gray-300 rounded-lg px-2 py-1" v-model="dossierBarcode" required>
                  <span class="danger">{{ errArray['status_error'] ? errArray['status_error'].toString() : '' }}</span>
                  <span class="danger">{{ errArray['detail'] ? errArray['detail'].toString() : '' }}</span>
                  <span id='err' class="danger"></span>
                  <span v-if="messege" class="danger">{{ messege }}</span>
              </form>
          </div>     
      </div>

      <!-- Tasks Lists -->

      <div v-if="tasks.length!=0 && !showForm" class="relative overflow-x-auto shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        Заявка
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Услуга
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Досье
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Срок исполнения
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Статус
                    </th>
                    <th scope="col" class="px-6 py-3">
                        <span class="sr-only">Детали</span>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="task in tasks" :key="task.id" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
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
                      <button v-if="task.request.service=='full_scanning' || task.request.service=='scanning_by_documents'"
                      @click="getScans(task)" class="rounded-md bg-indigo-600 px-3 py-2 text-xs font-semibold text-white shadow-sm hover:bg-indigo-500">
                        Исполнить
                      </button>
                      <button v-if="task.request.service=='temporary_issuance' || task.request.service=='unrecoverable_issuance'"
                      @click="addDossierToRegistry(task, 'rc')" class="rounded-md bg-indigo-600 px-3 py-2 text-xs font-semibold text-white shadow-sm hover:bg-indigo-500">
                        Добавить в реестр
                      </button>
                      <button v-if="!closeTaskForm" @click="closeTaskForm=true, currentTask=task" class="rounded-md bg-red-600 px-3 py-2 ml-2 text-xs font-semibold text-white shadow-sm hover:bg-red-500">
                        Закрыть
                      </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-if="closeTaskForm" class="mt-3 ml-3 flex flex-col">
          <form @submit.prevent="closeTask(currentTask, 'rejected')" class="w-full">
            <div>
              <label for="commentary" class="text-s">Введите причину закрытия задания по досье {{ currentTask.dossier }} из заявки {{ currentTask.request.id }}:</label>
              <input id="commentary" v-model="commentary" class="ml-5" required>
            </div>
              
            <div class="mt-5">  
              <button type="submit" class="float-left ml-2 mb-4 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500">
                  Закрыть задание
              </button>
              <button @click="closeTaskForm=false, commentary=''" class="float-left ml-2 mb-4 rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500">
                  Отмена
              </button>
            </div>
          </form>
        </div>
    </div>
    <div v-if="showForm" class="relative overflow-x-auto shadow-md sm:rounded-lg">

    <div class="flex flex-col">
      <div class="mt-1 ml-1">
        <button @click="showForm=false" class="float-left ml-2 rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500">
            Назад
        </button>
        <button @click="uploadForm=true" v-if="!uploadForm" class="float-left ml-2 rounded-md bg-green-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-400">
            Прикрепить скан
        </button>
      </div>
      <div class="flex">
        <div class=" mt-3 ml-3 mb-8 mr-12">
            <h2 class="text-xl font-bold mb-4">Описание задания</h2>
            <p>{{ currentTask.request.description }}</p>
        </div>

        
        <div v-if="!closeTaskForm2" class="mt-3 ml-3">
          <button @click="closeTaskForm2=true" class="float-left ml-2 rounded-md bg-blue-600 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-blue-500">
            Закрыть задание
          </button>
        </div>


        <div v-if="closeTaskForm2" class="mt-3 ml-3 flex flex-col">
          <form @submit.prevent="closeTask(currentTask, 'completed')" class="w-full">
            <div>
              <label for="commentary" class="text-l font-bold">Причина закрытия:</label>
              <input id="commentary" v-model="commentary" class="ml-5" required>
            </div>
              
            <div class="mt-5">  
              <button type="submit" class="float-left ml-2 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500">
                Закрыть
              </button>
              <button @click="closeTaskForm2=false, commentary=''" class="float-left ml-2 rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500">
                Отмена
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
      <div class="flex ml-3">

        <div class="w-1/3 mr-1 ml-1 mt-5 mb-12">
            <h2 class="text-l font-bold">Добавленные скан-копии:</h2>
            <ul>
                <li v-for="scan in scans" :key="scan.id">
                    <a :href="scan.file" target="_blank" class="text-blue-500 hover:text-blue-700">{{ scan.name }}</a>
                </li>
            </ul>
        </div>

        <div v-if="uploadForm" class="w-2/3 mr-1 ml-1 mt-5">
            <form @submit.prevent="uploadScan" class="w-full">
                <label for="fileInput" class="float-left ml-2 rounded-md bg-orange-600 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-orange-500">
                    Выбрать файл
                </label>
                <input type="file" id="fileInput" @change="handleFileChange" class="hidden" />
                <span class="ml-2">{{ scan.file.name }}</span>
                <div class="mt-2">
                    <label for="fileName">Название:</label>
                    <input type="text" id="fileName" v-model="scan.fileName" required class="w-full rounded-md border px-3 py-2" />
                </div>
                <div class="mt-2 mb-4">
                    <label for="fileDescription">Описание:</label>
                    <input type="text" id="fileDescription" v-model="scan.fileDescription" class="w-full rounded-md border px-3 py-2" />
                </div>
                <button type="submit" v-if="scan.file" class="float-right mt-3 mr-3 mb-3 rounded-md bg-green-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-400">
                    Загрузить
                </button>
            </form>
        </div>
      </div>
    </div>
    <div v-if="Object(this.registries).length !==0 && !showForm" class="relative overflow-x-auto shadow-md sm:rounded-lg">
            <h2 class="text-xl font-bold mb-2">Созданные реестры:</h2>
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
                        class="rounded-md bg-green-500 px-2 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-green-400">
                        Отправить  
                    </button>
                      </td>
                  </tr>
              </tbody>
          </table>
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
      scans: [],
      currentTask:{},
      showForm:false,
      closeTaskForm:false,
      closeTaskForm2:false,
      uploadForm:false,
      dossierBarcode:'',
      messege:'',
      commentary:'',
      scan:{
        'file':'',
        'fileName':'',
        'fileDescription':''
      },
      registries:[],
      errArray: [],
      }
  },


  methods: {

    findDossierTasks(){
      this.tasks = [];
      this.messege = '';
      this.showForm = false;
      this.currentTask = '';
      axios.get('/api/requests/execute-tasks/?dossier_barcode=' + this.dossierBarcode).then(
          response =>{
              console.log(response.data)
              this.tasks = response.data
              this.errArray = []
              if(this.tasks.length == 0){
                this.messege = 'По данному досье нет неисполненных заданий'
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

    getScans(task) {
      this.currentTask = task;
      axios.get('/api/units/scans/?dossier=' + this.currentTask.dossier)
        .then(response => {
          console.log(response.data)
          this.scans = response.data;
          this.showForm = true;
          this.uploadForm = false;
          this.scan = {
                        'file':'',
                        'fileName':'',
                        'fileDescription':''
                      };
        })
        .catch(error => {
          console.error('Error fetching scans:', error);
        });
    },

    handleFileChange(event) {
      this.scan.file = event.target.files[0];
    },

    uploadScan() {
      const formData = new FormData();
      formData.append('dossier', this.dossierBarcode.trim());
      formData.append('file', this.scan.file);
      formData.append('name', this.scan.fileName);
      formData.append('description', this.scan.fileDescription);
      formData.append('uploader', this.userStore.user.id);

      axios.post(`/api/units/scans/`, formData)
        .then(response => {
          console.log('Scan uploaded successfully', response.data);
          this.getScans(this.currentTask)
        })
        .catch(error => {
          console.error('Error uploading scan:', error);
        });
    },

    closeTask(taskToClose, status){
      axios.patch('/api/requests/tasks/'+ taskToClose.id + '/',
              {
              task_status:status,
              executor:this.userStore.user.id,
              commentary:this.commentary,
              }
                  ).then(response =>{
                          console.log(response.data);
                          this.closeTaskForm = false;
                          this.closeTaskForm2 = false;
                          this.showForm = false;
                          this.currentTask = {};
                          this.tasks = this.tasks.filter(task =>(task != taskToClose));
                          this.addDossierToRegistry(taskToClose, 'rl')
                          
                          }         
              ).catch(error =>{
                  console.log(error)
              }
          );
      this.commentary = '';
    },

    addDossierToRegistry(taskToRegistry, registryType){
      let registry = {
        'type':registryType,
        'status':'creation',
        'sender':this.userStore.user.id
      }
      axios.post(`/api/units/registry/?task_id=${taskToRegistry.id}`, registry
                  ).then(response =>{
                          console.log(response.data);
                          this.addRegistry(response.data)
                          this.tasks = this.tasks.filter(task =>(task != taskToRegistry));
                          
                          }         
              ).catch(error =>{
                  console.log(error)
              }
          );

    },

    addRegistry(registry) {
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
    },

    sendRegistry(registry){
        registry.status = 'sent';
        registry.sender = this.userStore.user.id
        axios.patch('/api/units/registry/' + registry.id + '/', registry).then(
            response =>{
                console.log(response.data);
                this.registries = this.registries.filter(reg =>(reg != registry));
            }
        ).catch(error =>{
            if (error.response) {
                console.log(error.response.data);
                this.errArray = error.response.data;
                }
            })
        },

  },

}
</script> 