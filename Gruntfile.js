module.exports = function (grunt) {
    grunt.initConfig({
        concat: {
            options: {
                separator: '\n\n'
            },
            dist: {
                src: [
                    'public/js/app/init.js',
                    'public/js/app/search.js',
                    'public/js/app/anagrams.js',
                    'public/js/app/app.js',
                    'public/js/app/socket.js'
                ],
                dest: 'public/js/valleyforge.js'
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