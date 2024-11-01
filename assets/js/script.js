$(document).ready(function () {
  // Плавная прокрутка при клике на ссылку
  $('a[href^="#"]').on("click", function (event) {
    var target = $(this.getAttribute("href"));

    if (target.length) {
      event.preventDefault();
      $("html, body").stop().animate(
        {
          scrollTop: target.offset().top,
        },
        1000
      );
    }
  });
});
$(document).ready(function() {
  // Открытие модального окна подарка
  $('#opengift').on('click', function() {
      $('#modal_gift').css('display', 'block');
      centerModal('#modal_gift .modal_gift_rect');
  });

  // Открытие модального окна помощи
  $('#openhelp').on('click', function() {
      $('#modal_help').css('display', 'block');
      centerModal('#modal_help .modal_help_rect');
  });

  // Закрытие модальных окон
  $('.modal_close').on('click', function() {
      $(this).closest('.modal_gift, .modal_help').css('display', 'none');
  });

  // Закрытие модальных окон при клике вне их
  $(window).on('click', function(event) {
      if ($(event.target).is('.modal_gift, .modal_help')) {
          $(event.target).css('display', 'none');
      }
  });

  // Функция для центрирования модального окна
  function centerModal(modalSelector) {
      var $modal = $(modalSelector);
      var top = ($(window).height() - $modal.outerHeight()) / 2;
      var left = ($(window).width() - $modal.outerWidth()) / 2;
      $modal.css({
          'top': top + 'px',
          'left': left + 'px',
          'position': 'fixed' // Убедитесь, что позиция фиксирована
      });
  }

  // Обновление позиции при изменении размера окна
  $(window).on('resize', function() {
      centerModal('#modal_gift .modal_gift_rect');
      centerModal('#modal_help .modal_help_rect');
  });
});