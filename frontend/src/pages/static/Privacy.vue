<template>
  <section class="static-page">
    <h1 class="page-title">Политика конфиденциальности</h1>
    <p class="intro">
      Мы бережно относимся к персональным данным и используем их только для обработки заказов, поддержки клиентов и улучшения сервиса.
    </p>
    <div class="content">
      <h2>Какие данные мы собираем</h2>
      <ul>
        <li>Контактные данные, которые вы оставляете при оформлении заказа или регистрации.</li>
        <li>История заказов и обращений в поддержку.</li>
        <li>Техническую информацию о работе сайта (cookies, данные аналитики).</li>
      </ul>

      <h2>Как мы используем данные</h2>
      <p>
        Данные помогают нам оформлять и доставлять заказы, отвечать на запросы, показывать актуальные предложения и предотвращать мошенничество.
      </p>

      <h2>Передача данных третьим лицам</h2>
      <p>
        Мы делимся данными только с партнёрами, которые участвуют в обработке заказов (службы доставки, платёжные системы). Мы требуем от них соблюдения всех норм конфиденциальности.
      </p>

      <h2>Ваши права</h2>
      <p>
        Вы можете запросить копию персональных данных, исправить их или удалить, а также отозвать согласие на маркетинговые рассылки.
      </p>

      <p class="contact">
        По вопросам конфиденциальности напишите нам на <a href="mailto:privacy@dronshop.ru">privacy@dronshop.ru</a>.
      </p>
    </div>
  </section>
</template>

<style scoped>
.static-page {
  @apply container mx-auto max-w-4xl px-4 py-10;
}

.page-title {
  @apply text-3xl font-bold mb-6;
}

.intro {
  @apply text-lg text-gray-600 mb-8;
}

.content h2 {
  @apply text-2xl font-semibold mt-8 mb-4;
}

.content ul {
  @apply list-disc pl-6 space-y-2 text-gray-700;
}

.content p {
  @apply text-gray-700 leading-relaxed;
}

.contact {
  @apply mt-8 text-gray-600;
}

.contact a {
  @apply text-accent hover:underline;
}
</style>
