/**
 * Created by budleigh on 7/11/16.
 */

Vue.config.delimiters = ['[[', ']]']; // clashes with template {}

Vue.component('search', {
    template: '#search',
    data: function () {
        return {
            words: ''
        }
    }
});

Vue.component('anagrams', {
    template: '#anagrams',
    data: function () {
        return {
            anagrams: []
        }
    }
});

var app = new Vue({
    el: '#app'
});