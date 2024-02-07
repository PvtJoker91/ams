<template>
    <div v-if="userStore.user.isAuthenticated && userStore.user.id" class="space-y-3">
      <h2 class="text-3xl font-bold mb-4">Комплектование архивного бокса</h2>
  
        <div class="p-6 bg-white border border-gray-200 rounded-lg">
            <div class="p-1 bg-white  rounded-lg">
                <form @submit.prevent="openArchiveBox" class="flex items-center">
                    <label class="form-label mr-2">Открыть архивный бокс:</label>
                    <input type="text" class="form-control border border-gray-300 rounded-lg px-2 py-1" v-model="archiveBox.barcode">
                    <span class="danger">{{ errArray['detail'] ? errArray['detail'].toString() : '' }}</span>
                    <span class="danger">{{ errArray['non_field_errors'] ? errArray['non_field_errors'].toString() : '' }}</span>
                    <span id='err' class="danger"></span>
                </form>
            </div>
    
            <div v-if="Object.keys(this.currentArchiveBox).length !== 0" class="mt-2">
              <button class="py-1 px-2 bg-purple-600 text-white rounded-lg shadow-sm hover:bg-purple-500" @click="closeArchiveBox()">Закрыть бокс</button>
            </div>
        
  
            <div class="p-1 bg-white  rounded-lg" v-if="Object.keys(this.currentArchiveBox).length !== 0">
                <form @submit.prevent="addOrRemoveDossier" class="flex items-center">
                    <label class="form-label mr-2">Введите ш/к для добавления/изъятия досье:</label>
                    <input type="text" class="form-control border border-gray-300 rounded-lg px-2 py-1" v-model="dossier.barcode">
                    <span class="danger">{{ errArray['dossier_status_error'] ? errArray['dossier_status_error'].toString() : '' }}</span>
                    <span class="danger">{{ errArray['non_field_errors'] ? errArray['non_field_errors'].toString() : '' }}</span>
                    <span class="danger">{{ errArray['validation_error'] ? errArray['validation_error'].toString() : '' }}</span>
                    <span id='err' class="danger"></span>
                </form>
            </div>
        </div>
  
        <!-- Dossiers Lists -->

        <div class="container mx-auto grid grid-cols-3 gap-4">
          <div v-if="Object(this.dossiers).length !== 0">
            <p class="text-l font-bold">Досье в боксе: ({{ dossiers.length }})</p>
            <ul>
              <li v-for="d in dossiers" class="mb-1">
                {{ d.barcode }}
              </li>
            </ul>
          </div>
  
          <div v-if="Object(this.addedDossiers).length !== 0">
            <p class="text-l font-bold">Добавленные досье: ({{ addedDossiers.length }})</p>
            <ul>
              <li v-for="d in addedDossiers" class="mb-1">
                {{ d.barcode }}
              </li>
            </ul>
          </div>
  
          <div v-if="Object(this.removedDossiers).length !== 0">
            <p class="text-l font-bold">Изъятые досье: ({{ removedDossiers.length }})</p>
            <ul>
              <li v-for="d in removedDossiers" class="mb-1">
                {{ d.barcode }}
              </li>
            </ul>
          </div>
        </div>
    </div>
    <div v-else>
      <AccessDenied />
    </div>
  </template>
  


<script>
import axios from 'axios'
import _ from 'lodash';
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
      currentArchiveBox: {},
      dossiers: [],
      addedDossiers: [],
      removedDossiers: [],
      'archiveBox': {
          'barcode':'',
          'status':'Under completion',
          'current_sector':'2',
          "storage_address":"",
      },
      'dossier':{
          'barcode':'',
          'current_sector':'2',
          'status':'',
          'archive_box':'',
      },
      'errArray': [],
      }
  },

  methods: {

  openArchiveBox(){
      axios.post('/api/logistics/completion/', this.archiveBox).then(
          response =>{
              console.log(response.data)
              this.currentArchiveBox = response.data
              this.dossiers = response.data.dossiers
              this.addedDossiers = []
              this.removedDossiers = []
              this.errArray = []
          }
      ).catch(error =>{
        if (error.response) {
      console.log(error.response.data);
      this.errArray = error.response.data;
      this.currentArchiveBox = {};
      this.dossiers = [];
    }
  }
  )

  },

  closeArchiveBox(){
    if (this.dossiers.length == 0 && this.addedDossiers.length == 0){
        axios.delete('/api/logistics/completion/' + this.currentArchiveBox.barcode + '/').then(
            response =>{
                console.log(response.data)
                this.removedDossiers = []
                this.currentArchiveBox = {}
            }
        ).catch(error =>{
            console.log(error)
        })
  
      } else {
      this.currentArchiveBox.status = 'Is completed'
      axios.post('/api/logistics/completion/', this.currentArchiveBox).then(
          response =>{
              console.log(response.data)
              this.dossiers = []
              this.addedDossiers = []
              this.removedDossiers = []
              this.currentArchiveBox = {}
          }
      ).catch(error =>{
          console.log(error)
      })
    }
    },

  isBarcodePresent(jsonData, barcodeToCheck) {
    return jsonData.some(obj => obj.barcode === barcodeToCheck);
    },

  addOrRemoveDossier(){
      let currentDossier = _.cloneDeep(this.dossier);
      if (
        !this.isBarcodePresent(this.dossiers, currentDossier.barcode) &&
        !this.isBarcodePresent(this.addedDossiers, currentDossier.barcode) &&
        !this.isBarcodePresent(this.removedDossiers, currentDossier.barcode)
        ){
            currentDossier.archive_box = this.currentArchiveBox.id;
            currentDossier.status = 'Added to a box';
            axios.patch('/api/logistics/completion/dossier/' +  currentDossier.barcode + '/', currentDossier).then(
            response =>{
                console.log(response.data)
                this.addedDossiers.push(currentDossier);
                this.errArray = [];
            }
        ).catch(error =>{
            if (error.response) {
                console.log(error.response.data);
                this.errArray = error.response.data;
                }
            }
        )
    }  else if (this.isBarcodePresent(this.dossiers, currentDossier.barcode)){
        currentDossier.archive_box = null;
        currentDossier.status = 'Removed from a box';
        this.makeRequest(currentDossier.barcode, currentDossier, this.dossiers, this.removedDossiers);


    } else if (this.isBarcodePresent(this.addedDossiers, currentDossier.barcode)){
        currentDossier.archive_box = null;
        currentDossier.status = 'Removed from a box';
        this.makeRequest(currentDossier.barcode, currentDossier, this.addedDossiers, this.removedDossiers);

    } else if (this.isBarcodePresent(this.removedDossiers, currentDossier.barcode)){
        currentDossier.archive_box = this.currentArchiveBox.id;
        currentDossier.status = 'Added to a box';
        this.makeRequest(currentDossier.barcode, currentDossier, this.removedDossiers, this.addedDossiers);
        
    };
      this.dossier.barcode = '';
    },

    makeRequest (barcode, dossier, from, to) {
      axios.patch('/api/logistics/completion/dossier/' +  barcode + '/', dossier).then(
          response =>{
              console.log(response.data);
              this.moveToDestination(dossier, from, to);
          }
      ).catch(error =>{
          console.log(error)
      });
    },
        
  moveToDestination(dossier, sourceArray, destinationArray) {
      const index = sourceArray.findIndex(i => i.barcode === dossier.barcode);
      sourceArray.splice(index, 1);
      destinationArray.push(dossier);
    },

}

}
</script>