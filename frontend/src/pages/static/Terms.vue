<template>
  <section class="static-page">
    <h1 class="page-title">Пользовательское соглашение</h1>
    <p class="intro">
      Используя DronShop, вы принимаете условия настоящего соглашения. Пожалуйста, прочитайте его перед оформлением заказов.
    </p>
    <div class="content">
      <h2>1. Общие положения</h2>
      <p>
        Интернет-магазин DronShop продаёт товары для FPV и хобби. Мы оставляем за собой право обновлять ассортимент и цены без дополнительного уведомления.
      </p>

      <h2>2. Заказ и оплата</h2>
      <p>
        Заказы принимаются через сайт круглосуточно. Оплата возможна онлайн или при получении — в зависимости от выбранного способа доставки.
      </p>

      <h2>3. Доставка и возврат</h2>
      <p>
        Сроки и стоимость доставки зависят от вашего региона и службы доставки. Возврат возможен в течение 14 дней при сохранении товарного вида и документов.
      </p>

      <h2>4. Ответственность</h2>
      <p>
        Мы не несем ответственности за действия третьих лиц и сбои коммуникаций. Однако всегда готовы помочь и решить спорные ситуации.
      </p>

      <h2>5. Контакты</h2>
      <p class="contact">
        По вопросам обслуживания пишите на <a href="mailto:support@dronshop.ru">support@dronshop.ru</a> или звоните +7 (999) 000-00-00.
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

.content p {
  @apply text-gray-700 leading-relaxed;
}

.contact a {
  @apply text-accent hover:underline;
}
</style>
