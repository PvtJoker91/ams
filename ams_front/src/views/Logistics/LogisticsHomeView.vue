<template>

    
    <div class="space-y-3">
            <h2 class="text-3xl font-bold mb-4">Логистика</h2>

        <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">
            <RouterLink to="/logistics/checking">
            <div class="main-left">
                <div class="p-12 bg-white border border-gray-200 rounded-lg text-center">
                    <h1 class="mb-6 text-2xl">Проверка комплектности</h1>
                </div>
            </div>
            </RouterLink>

            <RouterLink to="/logistics/completion">
            <div class="main-center">
                <div class="p-12 bg-white border border-gray-200 rounded-lg text-center">
                    <h1 class="mb-6 text-2xl">Комплектование</h1>
                </div>
            </div>
            </RouterLink>

            <RouterLink to="/logistics/placement">
            <div class="main-right">
                <div class="p-12 bg-white border border-gray-200 rounded-lg text-center">
                    <h1 class="mb-6 text-2xl">Размещение</h1>
                </div>
            </div>
            </RouterLink>
        </div>
    </div>



</template>
