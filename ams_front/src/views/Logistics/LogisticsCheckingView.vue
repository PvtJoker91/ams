<template>
    <div class="space-y-3">
      <h2 class="text-3xl font-bold mb-4">Проверка комплектности архивного бокса</h2>
        <div class="p-6 bg-white border border-gray-200 rounded-lg">
            <div class="p-1 bg-white  rounded-lg">
                <form @submit.prevent="openArchiveBox">
                    <label class="form-label mr-2">Открыть архивный бокс:</label>
                    <input type="text" class="border border-gray-300 rounded-lg px-2 py-1" v-model="archiveBox.barcode">
                    <span class="danger">{{ errArray['non_field_errors'] ? errArray['non_field_errors'].toString() : '' }}</span>
                    <span class="danger">{{ errArray['detail'] ? errArray['detail'].toString() : '' }}</span>
                    <span id="err" class="danger"></span>
                </form>
            </div>


            <div v-if="Object.keys(this.currentArchiveBox).length !== 0" class="mt-2">
                <button @click="closeArchiveBox" class="py-1 px-2 bg-purple-600 text-white rounded-lg">Завершить проверку</button>
            </div>


            <div class="p-1 bg-white rounded-lg" v-if="Object.keys(this.currentArchiveBox).length !== 0">
                <form id="dossierBarcodeForm" @submit.prevent="checkDossier" class="flex items-center">
                    <label class="form-label mr-2">Введите ш/к досье:</label>
                    <input type="text" class="border border-gray-300 rounded-lg px-2 py-1" v-model="dossier.barcode">
                    <span class="danger">{{ errArray['dossier_status_error'] ? errArray['dossier_status_error'].toString() : '' }}</span>
                    <span class="danger">{{ errArray['non_field_errors'] ? errArray['non_field_errors'].toString() : '' }}</span>
                    <span class="danger">{{ errArray['validation_error'] ? errArray['validation_error'].toString() : '' }}</span>
                    <span id="err" class="danger"></span>
                </form>
            </div>
        </div>

        <div v-if="message" class="p-6 bg-white border border-gray-200 rounded-lg">
                <p>В боксе остались несверенные досье. Желаете прервать проверку?</p>
                <button @click="closeArchiveBoxWithAError" class="py-1 px-2 bg-red-600 text-white rounded-lg mr-4">Прервать проверку</button>
                <button @click="message=false" class="py-1 px-2 bg-green-600 text-white rounded-lg">Продолжить проверку</button>
        </div>
    
        <div v-if="Object(this.dossiers).length !== 0 || Object(this.addedDossiers).length !== 0" class="p-6 bg-white border border-gray-200 rounded-lg">
            <div class="container mx-auto grid grid-cols-2 gap-4">
                <div v-if="Object(this.dossiers).length !== 0">
                <p class="text-l font-bold">Несверенные досье: ({{dossiers.length}})</p>
                <ul>
                    <li v-for="d in dossiers" class="mb-1">
                    {{ d.barcode }}
                    </li>
                </ul>
                </div>
        
                <div v-if="Object(this.checkedDossiers).length !== 0">
                    <p class="text-l font-bold">Сверенные досье: ({{checkedDossiers.length}})</p>
                    <ul>
                        <li v-for="d in checkedDossiers" class="mb-1">
                        {{ d.barcode }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
  </template>
  
  
  <script>
  import axios from 'axios'
  import _ from 'lodash';
  
  
  export default{
  
    data(){
        return{
        currentArchiveBox: {},
        currentDossier: {},
        dossiers: [],
        checkedDossiers: [],
        addedDossiers: [],
        message: false,
        'archiveBox': {
            'barcode':'',
            'status':'Under checking',
            'current_sector':'2',
            "storage_address":"",
        },
        'dossier':{
            'barcode':'',
            'current_sector':'2',
            'status':'',
            'archive_box':'',
            'contract':''
        },
        'errArray': [],
        }
    },
  
    methods: {
  
    openArchiveBox(){
        axios.patch('/api/logistics/checking/' + this.archiveBox.barcode + '/', this.archiveBox).then(
            response =>{
                console.log(response.data)
                this.currentArchiveBox = response.data
                this.dossiers = response.data.dossiers
                this.dossier.archive_box = this.currentArchiveBox
                this.currentDossier = {}
                this.checkedDossiers = []
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
        if (this.dossiers.length == 0){
        this.currentArchiveBox.status = 'Is checked'
        axios.patch('/api/logistics/checking/' + this.currentArchiveBox.barcode + '/', this.currentArchiveBox).then(
            response =>{
                console.log(response.data)
                this.checkedDossiers = []
                this.addedDossiers = []
                this.currentArchiveBox = {}
                this.currentDossier = {}
                this.archiveBox.barcode = ""
            }
        ).catch(error =>{
            console.log(error)
        })
  
      } else {
        this.message = true;
      }
    },

    closeArchiveBoxWithAError(){
        this.currentArchiveBox.status = 'Checked with an error'
        axios.patch('/api/logistics/checking/' + this.currentArchiveBox.barcode + '/', this.currentArchiveBox).then(
            response =>{
                console.log(response.data)
                this.checkedDossiers = []
                this.addedDossiers = []
                this.dossiers = []
                this.currentArchiveBox = {}
                this.currentDossier = {}
                this.archiveBox.barcode = ""
                this.message = false;
            }
        ).catch(error =>{
            console.log(error)
        })
  
    },

    isBarcodePresent(jsonData, barcodeToCheck) {
      return jsonData.some(obj => obj.barcode === barcodeToCheck);
      },
    
    moveToDestination(dossier, sourceArray, destinationArray) {
      const index = sourceArray.findIndex(i => i.barcode === dossier.barcode);
      sourceArray.splice(index, 1);
      destinationArray.push(dossier);
    },
    autoClose(){
        if(this.dossiers.length == 0){
            this.closeArchiveBox()
        }
    },
    checkDossier(){
        this.currentDossier = _.cloneDeep(this.dossier);
        if (
          !this.isBarcodePresent(this.dossiers, this.currentDossier.barcode) &&
          !this.isBarcodePresent(this.checkedDossiers, this.currentDossier.barcode)
            ){
                this.currentDossier.archive_box = this.currentArchiveBox.id;
                this.currentDossier.status = 'Checked in a box';
                axios.patch('/api/logistics/checking/dossier/' +  this.currentDossier.barcode + '/', this.currentDossier).then(
                response =>{
                    console.log(response.data)
                    this.addedDossiers.push(this.currentDossier);
                    this.checkedDossiers.push(this.currentDossier);
                    this.dossier.barcode = '';
                    this.errArray = [];
                }).catch(error =>{
                        if (error.response) {
                            console.log(error.response.data);
                            this.errArray = error.response.data;
                            }
                    })                      
      } else if (
          this.isBarcodePresent(this.dossiers, this.currentDossier.barcode) &&
          !this.isBarcodePresent(this.checkedDossiers, this.currentDossier.barcode)
            ){
                this.currentDossier.archive_box = this.currentArchiveBox.id;
                this.currentDossier.status = 'Checked in a box';
                axios.patch('/api/logistics/checking/dossier/' +  this.currentDossier.barcode + '/', this.currentDossier).then(
                response =>{
                    console.log(response.data);
                    this.moveToDestination(this.currentDossier, this.dossiers, this.checkedDossiers)
                    this.errArray = [];
                    this.dossier.barcode = '';
                    this.autoClose()
                }
            ).catch(error =>{
                if (error.response) {
                    console.log(error.response.data);
                    this.errArray = error.response.data;
                    }
                }
            )
      }  else if (this.isBarcodePresent(this.checkedDossiers, this.currentDossier.barcode)) {
            this.dossier.barcode = '';
        }
        }    
      }
    }
  </script>