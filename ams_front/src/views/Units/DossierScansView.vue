<template>
    <div v-if="userStore.user.isAuthenticated && userStore.user.id" class="space-y-3">
      <div v-if="Object.keys(dossier).length!==0">
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
                <div v-for="scan in dossier.scans" :key="scan.id" class="highlighted">
                    <ul>
                        <details>
                            <summary>
                                  <h2 class="text-m">Документ:         {{ scan.name }}</h2>
                            </summary>
                            <div class="mt-3 text-sm">
                                <li><a :href="scan.file" target="_blank" class="text-blue-500 hover:text-blue-700"><b>Открыть скан</b></a></li>
                                <li><b>Добавил:</b>     {{ scan.uploader.first_name }} {{ scan.uploader.last_name }}</li>
                                <li><b>Дата добавления:</b>     {{ scan.date_upload }}</li>
                                <li><b>Описание:</b>     {{ scan.description }}</li>
                            </div>
                        </details>
                    </ul>
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
          dossier:{},
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