<template>
  <div v-if="userStore.user.isAuthenticated && userStore.user.id" class="space-y-3"> 
      <h2 class="text-3xl font-bold mb-4">Размещение архивных боксов</h2>
        <div div class="p-1 bg-white  rounded-lg"> 
            <div v-if="successMessege">{{ successMessege }}</div>
            <form @submit.prevent="barcodeAddressDictMaker(insertForm)" class="mb-3 mt-3 ml-3 mr-3">
                <textarea rows="17" cols="30" class="border border-gray-300 rounded-lg" v-model="insertForm"
                placeholder=
"Введите штрихкод полки, затем 
штрихкоды архивных боксов, 
затем снова штрихкод полки 
каждый ш/к на новой строке 
Пример:
10.00.00.-A.00.01
AB-00-000001
AB-00-000002
AB-00-000003
10.00.00.-A.00.01
10.00.00.-A.00.02
AB-00-000004
AB-00-000005
AB-00-000006
10.00.00.-A.00.02"></textarea>
                <p><button type="submit" class="py-2 px-4 bg-blue-600 text-white rounded-lg mt-2 shadow-sm hover:bg-blue-500">Разместить на хранение</button></p>                                     
            </form>
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
        insertForm: '',
        barcodeAddressDict: {},
        "archiveBox": {
            "barcode":"",
            "current_sector":"2",
            "status":"Under storage",
            "shelf_code": ""
        },
        successMessege:'',
        }
    },

    methods: {

        barcodeAddressDictMaker(string){
            const result = {};
            const listBarcodeAddress = string.split("\n");
            let curShelf = listBarcodeAddress[0];
            let curBox = listBarcodeAddress[1];
            let i = 1;
            while (i < listBarcodeAddress.length - 1) {
                if (curBox !== curShelf) {
                    result[curBox] = curShelf;
                    curBox = listBarcodeAddress[i + 1];
                } else {
                    curShelf = listBarcodeAddress[i + 1];
                    curBox = listBarcodeAddress[i + 2];
                }
                i += 1;
            }

            this.barcodeAddressDict = result;
            if (result){this.placeArchiveBox(this.barcodeAddressDict)};
            
        },


        placeArchiveBox(dict){
            this.successMessege = '';
            let archiveBoxList = [];
            for (const [box, shelf] of Object.entries(dict)) {
            this.archiveBox.barcode = box;
            this.archiveBox.shelf_code = shelf;
            archiveBoxList.push(this.archiveBox)
            }
            axios.put('/api/logistics/placement', archiveBoxList).then(
                response =>{
                    console.log(response.data)
                    this.successMessege = 'Короба размещены!'
                }
            ).catch(error =>{
                console.log(error)
            })

            this.insertForm = ''
        },
    }
  

}
</script>