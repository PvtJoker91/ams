<template>
    <div class="space-y-3">
        <h2 class="text-3xl font-bold mb-8">Карточка досье {{dossier.barcode}}</h2>
        <div class="flex">

            <div class="flex-1 mt-6">
                <h2 class="text-xl font-bold mb-4">Информация о договоре:</h2>
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
                <div>
                    <b class="block">Дата регистрации: </b>
                    <span class="block">{{ dossier.registration_date }}</span>
                </div>
                <div>
                    <b class="block">Регистратор: </b>
                    <span class="block">{{ dossier.registerer.first_name }} {{ dossier.registerer.last_name}}</span>
                </div>
            </div>
            <div class="flex-1 mt-6">
                <h2 class="text-xl font-bold mb-4">Добавленные скан-копии:</h2>
                <div v-for="scan in dossier.scans">
                    <span class="block">
                        <a :href="scan.file" target="_blank" class="text-blue-500 hover:text-blue-700">{{ scan.name }}</a>
                        {{ scan.description }} {{ scan.uploader }} {{ scan.date_upload }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>
    
<script>
    import axios from 'axios';
    
    export default {
      data() {
        return {
          dossier:{
            'contract':{
                'client':{},
                'product':{}
              },
            'registerer':{
              'last_name':'',
              'first_name':'',
            },
            'scans': [],
          },
        }
      },


      mounted() {
        this.getDossier();
      },
  
      methods: {
        getDossier(){
            axios.get('/api/units/dossier-scans/'+ this.$route.params.barcode + '/',)
         .then(response => {
            console.log(response.data);
            this.dossier = response.data;

        }).catch(error =>{
                    console.log(error)
        })
        }
    }
}
    
</script>