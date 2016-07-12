module.exports = function (grunt) {
    grunt.initConfig({
        concat: {
            options: {
                separator: '\n\n'
            },
            dist: {
                src: [
                    'src/js/init.js',
                    'src/js/search.js',
                    'src/js/anagrams.js',
                    'src/js/app.js',
                    'src/js/socket.js'
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