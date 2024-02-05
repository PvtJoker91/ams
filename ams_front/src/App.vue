<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 text-white">
      <div class="py-5 px-8 border-b border-gray-700">
        <RouterLink to="/" class="text-xl block">СУАД</RouterLink>
      </div>

      <div class="py-5 px-8">
        <template v-if="userStore.user.isAuthenticated">


          <div class="block py-2">
              <span class="cursor-pointer" @click="toggleRequestsMenu">Создание заявок</span>
            <ul v-show="requestsMenuOpen" class="pl-4">
              <li><RouterLink to="/requests/create">Создать заявку</RouterLink></li>
              <li><RouterLink to="/requests/myrequests">Мои заявки</RouterLink></li>
            </ul>
          </div>

          <div class="block py-2">
          <RouterLink to="/registration">Регистрация</RouterLink>
          </div>
          
          <div class="block py-2">
            <span class="cursor-pointer" @click="toggleLogisticsMenu">Логистика</span>
            <ul v-show="logisticsMenuOpen" class="pl-4">
              <li><RouterLink to="/logistics/checking">Проверка бокса</RouterLink></li>
              <li><RouterLink to="/logistics/completion">Комплектование</RouterLink></li>
              <li><RouterLink to="/logistics/placement">Размещение</RouterLink></li>
            </ul>
          </div>

          <div class="block py-2">
            <span class="cursor-pointer" @click="toggleSelectionMenu">Подбор досье</span>
            <ul v-show="selectionMenuOpen" class="pl-4">
              <li><RouterLink to="/selection/orders">Наряды на подбор</RouterLink></li>
              <li><RouterLink to="/selection/create">Создание наряда</RouterLink></li>
              <li><RouterLink to="/selection/execute">Исполнение нарядов</RouterLink></li>
            </ul>
          </div>
          
          <div class="block py-2">
            <span class="cursor-pointer" @click="toggleRequestsFulfillmentMenu">Обработка заявок</span>
            <ul v-show="requestsFulfillmentMenuOpen" class="pl-4">
              <li><RouterLink to="/requests/list">Заявки</RouterLink></li>
              <li><RouterLink to="/requests/tasks">Задания по заявкам</RouterLink></li>
              <li><RouterLink to="/requests/tasks/execution">Исполнение заданий</RouterLink></li>
            </ul>
          </div>

          <div class="block py-2">
            <RouterLink to="/units/registry">Реестры</RouterLink>
          </div>

          <div class="block py-2">
            <RouterLink to="/units/card/">Карточка ЕХ</RouterLink>
          </div>

        </template>
      </div>

      <div class="py-20 px-8 mt-auto text-xs">
        <template v-if="userStore.user.isAuthenticated && userStore.user.id">
             {{ userStore.user.first_name }} {{ userStore.user.last_name }}

          <button @click="logout()" class="inline-block py-2 px-1 bg-red-800 text-xs text-white rounded-lg shadow-sm hover:bg-red-700">
              Log out
          </button>
        </template>
      </div>
    </aside>

    <main class="flex-1 bg-white px-8 py-5">
      <RouterView />
    </main>

  </div>
</template>

<script>
  import axios from 'axios'
  import { useUserStore } from './stores/user'

  export default {
      setup() {
          const userStore = useUserStore()
          return {
              userStore
          }
      },

      components: {
      },

      beforeCreate() {
          this.userStore.initStore()

          const token = this.userStore.user.access

          if (token) {
              axios.defaults.headers.common["Authorization"] = "Bearer " + token;
          } else {3
              axios.defaults.headers.common["Authorization"] = "";
          }
      },

      data() {
        return {
          logisticsMenuOpen: false,
          selectionMenuOpen: false,
          requestsMenuOpen: false,
          requestsFulfillmentMenuOpen: false,
        };
      },
      methods: {
        toggleLogisticsMenu() {
          this.logisticsMenuOpen = !this.logisticsMenuOpen;
        },
        toggleSelectionMenu() {
          this.selectionMenuOpen = !this.selectionMenuOpen;
        },
        toggleRequestsMenu() {
          this.requestsMenuOpen = !this.requestsMenuOpen;
        },
        toggleRequestsFulfillmentMenu() {
          this.requestsFulfillmentMenuOpen = !this.requestsFulfillmentMenuOpen;
        },
        hasGroup(groupName) {
            return this.userStore.user && this.userStore.user.groups.some(group => group.name === groupName);
        },
        logout() {
            console.log('Log out')

            this.userStore.removeToken()

            this.$router.push('/')
        }

      },
  }
</script>