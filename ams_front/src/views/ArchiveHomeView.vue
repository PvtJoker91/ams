<template>
    <div v-if="userStore.user.isAuthenticated && userStore.user.id" class="space-y-3">
        <h2 class="text-3xl font-bold mb-4">Выполнение задач архива</h2>
        <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">
            <RouterLink to="/registration">
            <div class="main-left">
                <div class="p-12 bg-white border border-gray-200 rounded-lg text-center">
                    <h1 class="mb-6 text-2xl">Регистрация</h1>
                </div>
            </div>
            </RouterLink>

            <RouterLink to="/logistics">
            <div class="main-center">
                <div class="p-12 bg-white border border-gray-200 rounded-lg text-center">
                    <h1 class="mb-6 text-2xl">Логистика</h1>
                </div>
            </div>
            </RouterLink>

            <RouterLink to="/requests/fulfillment">
            <div class="main-right">
                <div class="p-12 bg-white border border-gray-200 rounded-lg text-center">
                    <h1 class="mb-6 text-2xl">Обработка заявок</h1>
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
import AccessDenied from '../components/AccessDenied.vue';
import { useUserStore } from '../stores/user';

export default {
    
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