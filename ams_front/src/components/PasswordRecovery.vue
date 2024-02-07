<template>
    <div class="main-right">
            <div v-if="!successMessage" class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="recoverPassword">
                    <div>
                        <label>Введите Email для сброса пароля</label><br>
                        <input type="email" v-model="email" required placeholder="Ваш Email" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>
                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg shadow-sm hover:bg-purple-500">Отравить</button>
                    </div>
                </form>
            </div>
            <div v-if="successMessage" class="bg-green-300 text-white rounded-lg p-6">
                <p>{{ successMessage }}</p>
            </div>
        </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        email: '',
        successMessage: '',
      };
    },

    methods: {
      async recoverPassword() {
        await axios.post('/api/users/password-recovery/', {'email': this.email})
            .then(response => {
                console.log(response.data.message);
                this.successMessage = response.data.message;
                
            })
            .catch(error => {
                console.error('Ошибка восстановления пароля:', error);
            })

      },
    },
  };
  </script>