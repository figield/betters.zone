'use strict'
import '../css/main.scss';
import './analytics.js';

Date.prototype.toDateInputValue = (function () {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
});
$(document).ready(function (e) {
    application.init();
    application.setDefaultDate();
    application.changeTime();
});

var application = {
    init: function () {
        this.events();
    },
    currentTime: function () {
        var d = new Date();
        var h = d.getHours();
        var m = d.getMinutes();
        var now;

        if (h < 10) h = '0' + h;
        if (m < 10) m = '0' + m;

        now = h + ':' + m;
        return now;
    },
    setDefaultDate: function () {
        $('#id_start_date').val(new Date().toDateInputValue());
        $('input[type="time"]').val(this.currentTime());
    },
    disableScroll: function () {
        $('body').toggleClass('prevent-scroll');
    },
    changeTime: function (e) {
        var chosenTime = $('input[type="time"]').val();
        var hours;
        var minutes;

        if (chosenTime) {
            hours = chosenTime.substr(0, 2);
            minutes = chosenTime.substr(3, 5);

            $('#hours').val(hours);
            $('#minutes').val(minutes);
        }
    },
    changePlaceholder: function () {
        var uploadInput = $('#id_photo').val();
        var placeholderInput = $('#placeholder_input');

        placeholderInput.val(uploadInput);
    },
    showSection: function (element, otherTrigger) {
        var triggerId = '#' + otherTrigger;
        var isTriggerOpen = $('label[for="' + otherTrigger + '"] span').hasClass('fa-close');

        if (isTriggerOpen) {
            $(triggerId).click();
        }

        // $(element).toggleClass('hidden');
        $(element).toggleClass('mobile-hidden');
    },
    preventScroll: function () {
        $('body').toggleClass('prevent-scroll');
    },
    makeCloseIcon: function (parent, child) {
        $(parent).toggleClass(child);
    },
    changeTab: function (e) {
        var tabId = $(e.target).attr('data-tab');

        $('ul.tabs li').removeClass('current');
        $('.tab-content').removeClass('current');

        $(e.target).addClass('current');
        $("#" + tabId).addClass('current');
    },
    addLoader: function () {
        $('body .loader').css( "display", "block" );
    },
    enableAcceptButton: function(e) {
        var acceptButton = $(e.currentTarget).closest('form').find('button[type="submit"]');

        if($(e.currentTarget).is(':checked')) {
            $(acceptButton).attr("disabled", false);
        } else {
            $(acceptButton).attr("disabled", true);
        }
    },
    checkIfItIsANumber: function (inputValue) {
        var intRegex = /^[1-9]?[0-9]$/;
        if(intRegex.test(inputValue)){
            return inputValue;
        } else {
            return null;
        }
    },
    changeScoreUp: function() {
        var self = $(this);
        var scoreInput = self.next();
        var scoreValue = scoreInput.val();
        var returnedValue = application.checkIfItIsANumber(scoreValue);
        if(!returnedValue || (returnedValue && returnedValue >= 99)) {
            scoreInput.val(0);
        } else {
            returnedValue = parseInt(returnedValue);
            scoreInput.val(returnedValue += 1);
        }
    },
    changeScoreDown: function() {
        var self = $(this);
        var scoreInput = self.prev();
        var scoreValue = scoreInput.val();
        var returnedValue = application.checkIfItIsANumber(scoreValue);
        if(!returnedValue || (returnedValue && returnedValue <= 0)) {
            scoreInput.val(0);
        } else {
            scoreInput.val(returnedValue -= 1);
        }
    },
    clearInput: function() {
        var self = $(this);
        var scoreValue = self.val();
        var returnedValue = application.checkIfItIsANumber(scoreValue);
        self.val(returnedValue);
    },
    highlightCurrentLink: (function () {
      var mainMenuLinks = $('.main-nav-links').find('a');
      mainMenuLinks.each(function(){
        if ($(this).prop('href') == window.location.href) {
          $(this).addClass('active-link-main-menu'); 
        }
      });
    })(),
    events: function () {
        var self = this;
        var scoreUpButton = $('.current-round-score-up');
        var scoreDownButton = $('.current-round-score-down');
        var scoreInput = $('.current-round-score').find('input');

        $('#id_start_time').on('change', function () {
            self.changeTime();
        })

        $('#id_photo').on('change', function () {
            self.changePlaceholder();
        })

        $('#menu-x').on('change', function () {
            self.makeCloseIcon('.mobile-menu .x span', 'fa-bars fa-close');
            self.showSection('#main-nav-links', 'menu-login');
            self.preventScroll();
        })

        $('#menu-login').on('change', function () {
            self.makeCloseIcon('.mobile-login span', 'fa-user fa-close');
            self.showSection('#main-login-form', 'menu-x');
            self.preventScroll();
        })

        $('ul.tabs li').on('click', function (e) {
            self.changeTab(e);
        })

        $('.save, .fa-close').on('click', function() {
            self.addLoader();
        })

        $('#termsaccept').on('change', function(e) {
            self.enableAcceptButton(e);
        })

        scoreUpButton.on("click", application.changeScoreUp);
        scoreDownButton.on("click", application.changeScoreDown);
        scoreInput.on("keyup", application.clearInput);
    }
};
