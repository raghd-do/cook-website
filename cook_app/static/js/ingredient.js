console.log("loaded from Static JS file");
$.fn.select2.defaults.set('amdLanguageBase', 'select2/i18n/');

$(document).ready(function () {
    $('.select-ingredients').select2({
      placeholder: 'Select or add ingredients',
      tags: true,
      tokenSeparators: [',', '/'],
      allowClear: true,
      theme: "classic",
      "pagination": {
        "more": true,
      }
    });
  });