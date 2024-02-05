import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import ArchiveHomeView from '../views/ArchiveHomeView.vue'
import RequestsHomeView from '../views/Requests/RequestsHomeView.vue'
import RequestCreateView from '../views/Requests/RequestCreateView.vue'
import RequestListView from '../views/Requests/RequestListView.vue'
import MyRequestsView from '../views/Requests/MyRequestsView.vue'
import RequestDetailView from '../views/Requests/RequestDetailView.vue'
import RequestsFulfillmentView from '../views/Requests/RequestsFulfillmentView.vue'
import TasksView from '../views/Requests/TasksView.vue'
import TaskExecutionView from '../views/Requests/TaskExecutionView.vue'
import LogisticsHomeView from '../views/Logistics/LogisticsHomeView.vue'
import LogisticsCompletionView from '../views/Logistics/LogisticsCompletionView.vue'
import LogisticsPlacementView from '../views/Logistics/LogisticsPlacementView.vue'
import LogisticsCheckingView from '../views/Logistics/LogisticsCheckingView.vue'
import SelectionHomeView from '../views/Selection/SelectionHomeView.vue'
import SelectionOrderListView from '../views/Selection/SelectionOrderListView.vue'
import SelectionOrderCreateView from '../views/Selection/SelectionOrderCreateView.vue'
import SelectionOrderExecuteView from '../views/Selection/SelectionOrderExecuteView.vue'
import SelectionOrderPrintView from '../views/Selection/SelectionOrderPrintView.vue'
import RegistrationView from '../views/Registration/RegistrationView.vue'
import EXDetailView from '../views/Units/EXDetailView.vue'
import RegistryListView from '../views/Units/RegistryListView.vue'
import RegistryDetailView from '../views/Units/RegistryDetailView.vue'
import DossierScansView from '../views/Units/DossierScansView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/reset-password/:uidb64/:token',
      name: 'resetPassword',
      component: ResetPasswordView
    },
    {
      path: '/requests',
      name: 'requests',
      component: RequestsHomeView
    },
    {
      path: '/requests/create',
      name: 'requestCreate',
      component: RequestCreateView
    },
    {
      path: '/requests/list',
      name: 'requestList',
      component: RequestListView
    },
    {
      path: '/requests/myrequests',
      name: 'myRequests',
      component: MyRequestsView
    },
    {
      path: '/requests/:id',
      name: 'requestDetail',
      component: RequestDetailView
    },
    {
      path: '/requests/fulfillment',
      name: 'requestsFulfillment',
      component: RequestsFulfillmentView
    },
    {
      path: '/requests/tasks',
      name: 'requestTasks',
      component: TasksView
    },
    {
      path: '/requests/tasks/execution',
      name: 'taskExecution',
      component: TaskExecutionView
    },
    {
      path: '/archive',
      name: 'archive',
      component: ArchiveHomeView
    },    
    {
      path: '/registration',
      name: 'registration',
      component: RegistrationView
    },
    {
      path: '/logistics',
      name: 'logistics',
      component: LogisticsHomeView
    },
    {
      path: '/logistics/completion',
      name: 'completion',
      component: LogisticsCompletionView
    },
    {
      path: '/logistics/placement',
      name: 'placement',
      component: LogisticsPlacementView
    },
    {
      path: '/logistics/checking',
      name: 'checking',
      component: LogisticsCheckingView
    },
    {
      path: '/selection',
      name: 'selection',
      component: SelectionHomeView
    },
    {
      path: '/selection/create',
      name: 'selectionOrderCreate',
      component: SelectionOrderCreateView
    },
    {
      path: '/selection/execute',
      name: 'selectionOrderExecute',
      component: SelectionOrderExecuteView
    },
    {
      path: '/selection/orders',
      name: 'selectionOrderList',
      component: SelectionOrderListView
    },
    {
      path: '/selection/orders/:id',
      name: 'selectionOrderPrint',
      component: SelectionOrderPrintView
    },
    {
      path: '/units/card',
      name: 'eXCard',
      component: EXDetailView
    },
    {
      path: '/units/registry',
      name: 'registryList',
      component: RegistryListView
    },
    {
      path: '/units/registry/:id',
      name: 'registryDetail',
      component: RegistryDetailView
    },
    {
      path: '/units/dossier/:barcode',
      name: 'dossierScans',
      component: DossierScansView
    },

  ]
})

export default router
