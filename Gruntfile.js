module.exports = function (grunt) {
    grunt.initConfig({
        concat: {
            options: {
                // change this when minified
                // for now this is to make
                // it readable post-concat
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

    // below can be run manually and is automatically
    // called on heroku by sticking it into the
    // post-install script in package.json
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.registerTask('build', [
        'concat'
    ]);
    grunt.registerTask('default', [
        'build'
    ]);
};