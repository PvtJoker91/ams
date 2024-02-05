<template>    
    <h2 class="text-3xl font-bold mb-8">Наряд на подбор {{ order.id }}</h2>
    <div>
        <button @click="printData" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Print</button>
        <table ref="printTable" class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        N
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Топография
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Архивный бокс
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Досье
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Статус досье
                    </th>     
                </tr>
            </thead>
            <tbody>
                <tr v-for="task, num in order.tasks" :key="task.dossier.barcode" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <th scope="row" class="px-6 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{num + 1}}
                    </th>
                    <td class="px-6 py-3">
                        <div v-if="task.dossier.archive_box!=null &&task.dossier.archive_box.storage_address!=null">{{ task.dossier.archive_box.storage_address.shelf_code }}</div>
                    </td>
                    <td class="px-6 py-3">
                        <div v-if="task.dossier.archive_box!=null">{{ task.dossier.archive_box.barcode }}</div>
                    </td>
                    <td class="px-6 py-3">
                        {{ task.dossier.barcode }}
                    </td>
                    <td class="px-6 py-3">
                        {{ task.dossier.status }}
                    </td>
                </tr>
            </tbody>
            
        </table>
    
    </div>
</template>


<script>
import axios from 'axios'

export default {

    data() {
        return {
            order:{}
        }
    },

    mounted(){
        this.getOrder()
    },

    methods: {
        getOrder() {
            axios
                .get(`/api/selection/orders/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)
                    this.order = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        printData() {
            var divToPrint = this.$refs.printTable;
            var newWin = window
            newWin.document.write(divToPrint.outerHTML);
            newWin.print();
        },
    },
}
</script>