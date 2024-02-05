<template>

    <div class="max-w-7xl bg-white text-center">
        <h1 class="mb-6 text-2xl">Добро пожаловать в Систему Управления Архивными Документами!</h1>
    

    <div v-if="userStore.user.isAuthenticated && userStore.user.id" class="max-w-7xl bg-white text-center">
        <h3 class="mb-6 text-xl text-gray-500">Выберите раздел:</h3>
        <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
            <RouterLink to="/requests">
            <div class="main-left">
                <div class="p-12 bg-white border border-gray-200 rounded-lg text-center ml-5 mb-5">
                    <h1 class="mb-6 text-2xl">Создание заявок в архив</h1>
                </div>
            </div>
            </RouterLink>

            <RouterLink to="/archive">
            <div class="main-right">
                <div class="p-12 bg-white border border-gray-200 rounded-lg text-center mr-5 mb-5">
                    <h1 class="mb-6 text-2xl">Выполнение задач архива</h1>
                </div>
            </div>
            </RouterLink>
        </div>
    </div>

    <div v-else class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <p class="mb-6 text-gray-500"> Для получения доступа, пожалуйста, войдите в систему!</p>
            </div>
        </div>

        <div v-if="!passChange" class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitLogInForm">
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="logInForm.email" placeholder="Ваш адрес электронной почты" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Пароль</label><br>
                        <input type="password" v-model="logInForm.password" placeholder="Ваш пароль" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button type='submit' class="py-4 px-6 mr-6 bg-purple-600 text-white rounded-lg shadow-sm hover:bg-purple-500">Войти</button>
                        <button @click="passChange=true" class="py-4 px-6 bg-red-700 text-white rounded-lg shadow-sm hover:bg-red-600">Сбросить пароль</button>
                    </div>
                    <div>
                        
                    </div>
                </form>
            </div>
        </div>
        <div v-if="passChange" class="main-right col-span-1 space-y-4">
            <PasswordRecovery />
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import PasswordRecovery from '../components/PasswordRecovery.vue';

import { useUserStore } from '../stores/user'

export default {
    
    components: {
        PasswordRecovery,
    },
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            logInForm: {
                email: '',
                password: '',
            },
            passChange: false,
            errors: []
        }
    },
    methods: {
        async submitLogInForm() {
            this.errors = []

            if (this.logInForm.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.logInForm.password === '') {
                this.errors.push('Your password is missing')
            }

            if (this.errors.length === 0) {
                await axios
                    .post('/api/auth/jwt/create/', this.logInForm)
                    .then(response => {
                        this.userStore.setToken(response.data)

                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
                    })
                    .catch(error => {
                        console.log('error', error)

                        this.errors.push('The email or password is incorrect!')
                    })
            }
            
            if (this.errors.length === 0) {
                await axios
                    .get('/api/users/me/')
                    .then(response => {
                        this.userStore.setUserInfo(response.data)
                        this.$router.push('/')
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        },

        submitChangePasswordForm() {
            this.errors = []

            if (this.changePasswordForm.password1 !== this.changePasswordForm.password2) {
                this.errors.push('Пароли не совпадают!')
            }

            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('old_password', this.changePasswordForm.old_password)
                formData.append('new_password1', this.changePasswordForm.new_password1)
                formData.append('new_password2', this.changePasswordForm.new_password2)

                axios
                    .post('/api/users/change-password/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.$router.push('/')
                        } else {
                            const data = JSON.parse(response.data.message)
                            for (const key in data){
                                this.errors.push(data[key][0].message)
                            }
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>