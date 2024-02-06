<template>
    <div v-if="userStore.user.isAuthenticated && userStore.user.id" class="space-y-3">
        <h2 class="text-3xl font-bold mb-4">Обработка заявок</h2>


        <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">
            <RouterLink to="/requests/list">
            <div class="main-left">
                <div class="p-8 bg-white border border-gray-200 rounded-lg text-center">
                    <h1 class="mb-6 text-2xl">Заявки</h1>
                </div>
            </div>
            </RouterLink>
            
            <RouterLink to="/requests/tasks">
            <div class="main-middle">
                <div class="p-8 bg-white border border-gray-200 rounded-lg text-center">
                    <h1 class="mb-6 text-2xl">Задания по заявкам</h1>
                </div>
            </div>
            </RouterLink>

            <RouterLink to="/requests/tasks/execution">
            <div class="main-right">
                <div class="p-8 bg-white border border-gray-200 rounded-lg text-center">
                    <h1 class="mb-6 text-2xl">Исполнение заданий</h1>
                </div>
            </div>
            </RouterLink>
        
        </div>
    </div>
    <div v-else>
      <AccessDenied />
    </div>
    
  </template>
    
    
  <script>
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
    }
   </script> 