module.exports = function (grunt) {
    grunt.initConfig({
        concat: {
            options: {
                separator: '\n\n'
            },
            dist: {
                src: [
                    'static/js/app/init.js',
                    'static/js/app/search.js',
                    'static/js/app/anagrams.js',
                    'static/js/app/app.js',
                    'static/js/app/util.js'
                ],
                dest: 'static/js/valleyforge.js'
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.registerTask('build', [
        'concat'
    ]);
    grunt.registerTask('default', [
        'build'
    ]);
};