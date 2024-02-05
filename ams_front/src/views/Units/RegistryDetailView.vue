<template>
    <h2 class="text-3xl font-bold mb-8">Реестр {{registry.type}} № {{registry.id}}</h2>
      <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                      №
                    </th>
                    <th scope="col" class="px-6 py-3">
                      Досье
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="dossier, number in dossiers" :key="number" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <th scope="row" class="px-6 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                      {{ number + 1 }}
                    </th>
                    <td class="px-6 py-3">
                      {{ dossier }}
                    </td>
                </tr>
            </tbody>
          </table>
      </div>
    
    </template>
    
    
    <script>
    import axios from 'axios'
    
    export default{

      data(){
          return{
          registry: {},
          dossiers: [],
          }
      },

      mounted() {
        this.getRegistry();
      },
    
      methods: {
        getRegistry(){
            axios.get('/api/units/registry/' + this.$route.params.id + '/',
                        ).then(response =>{
                                console.log(response.data)
                                this.registry = response.data
                                this.dossiers = response.data.dossiers
                                }         
                    ).catch(error =>{
                        console.log(error)
                    })
        },
      }
    
    }
    </script> 
    
      