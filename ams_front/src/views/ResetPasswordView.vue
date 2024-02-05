<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Смена пароля</h1>

                <p class="mb-6 text-gray-500">
                    Заполните форму для изменения вашего пароля!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitChangePasswordForm">
                    <div>
                        <label>Новый пароль</label><br>
                        <input type="password" v-model="new_password1" placeholder="Ваш новый пароль" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>
                    
                    <div>
                        <label>Повторите новый пароль</label><br>
                        <input type="password" v-model="new_password2" placeholder="Повторите ваш новый пароль" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div v-if="successMessage" class="bg-green-300 text-white rounded-lg p-6">
                        <p>{{ successMessage }}</p>
                    </div>
    
            
                    <div v-if="errors.length > 0" class="bg-red-300 text-white rounded-lg p-6">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
            

                    <div v-if="!successMessage">
                        <button type="submit" class="py-4 px-6 bg-purple-600 text-white rounded-lg hover:bg-purple-500">Сменить пароль</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    created() {
        this.getRouteParams()
    },

    data() {
        return {
            uidb64:'',
            token:'',
            new_password1: '',
            new_password2: '',
            successMessage: '',
            errors: []
        }
    },
    methods: {
        getRouteParams() {
            this.uidb64 = this.$route.params.uidb64;
            this.token = this.$route.params.token;
            },

        submitChangePasswordForm() {
            this.errors = []

            if (!this.new_password1) {
                this.errors.push('Пароль не может быть пустым!')
            }
            if (this.new_password1 !== this.new_password2) {
                this.errors.push('Пароли не совпадают!')
            }

            if (this.errors.length === 0) {
                let formData = {
                    "uidb64": this.uidb64,
                    "token": this.token,
                    "new_password": this.new_password1
                }
                axios
                    .post('/api/users/password-confirm-reset/', formData, {
                    })
                    .then(response => {
                        console.log(response.data);
                        this.successMessage = response.data.message;
                        this.new_password1 = '',
                        this.new_password2 = '',
                        setTimeout(() => {
                                this.$router.push('/');
                                 }, 1000);
                        
                    })
                    .catch(error => {
                        if (error.response) {
                            const data = error.response.data
                            console.log('error', data)
                            for (const key in data){
                                for (error in data[key]){
                                    this.errors.push(data[key][error])
                                }
                            }
                        }

                    })
            }
        }
    }
}
</script>