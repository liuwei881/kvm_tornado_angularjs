var tests = [];
for (var file in window.__karma__.files) {
  if (window.__karma__.files.hasOwnProperty(file)) {
    // Removed "Spec" naming from files
    if (/Spec\.js$/.test(file)) {
      tests.push(file);
    }
  }
}

requirejs.config({
    // Karma serves files from '/base'
    baseUrl: '/base/app/scripts',

    paths: {
        angular: '../../asserts/angular/angular',
        'angular-animate': '../../asserts/angular-animate/angular-animate',
        'angular-cookies': '../../asserts/angular-cookies/angular-cookies',
        'angular-mocks': '../../asserts/angular-mocks/angular-mocks',
        'angular-sanitize': '../../asserts/angular-sanitize/angular-sanitize',
        bootstrap: '../../asserts/bootstrap/dist/js/bootstrap',
        'angular-ui-router': '../../asserts/angular-ui-router/release/angular-ui-router',
        'angular-route': '../../asserts/angular-route/angular-route',
        jquery: '../../asserts/jquery/dist/jquery',
        'jquery-ui': '../../asserts/jquery-ui/jquery-ui',
        bootstraphoverdropdown: '../../asserts/metronic/global/plugins/bootstrap-hover-dropdown/bootstrap-hover-dropdown.min',
        slimscroll: '../../asserts/metronic/global/plugins/jquery-slimscroll/jquery.slimscroll.min',
        metronic: '../../asserts/metronic/global/metronic',
        layout: '../../asserts/metronic/admin/layout/layout',
        'angular-resource': '../../asserts/angular-resource/angular-resource',
        'angular-bootstrap': '../../asserts/angular-bootstrap/ui-bootstrap-tpls',
        'bootstrap-tpls': '../../asserts/angular-bootstrap/ui-bootstrap-tpls.min',
        typeAttrEtc: '../../asserts/etc/attrsConf',
        'highcharts-ng': '../../asserts/highcharts-ng/dist/highcharts-ng',
        highcharts: '../../asserts/highcharts-ng/highcharts'
    },

    shim: {
        'angular' : {'exports' : 'angular'},
        'angular-cookies': ['angular'],
        'angular-sanitize': ['angular'],
        'angular-resource': ['angular'],
        'angular-animate': ['angular'],
        'angular-mocks': {
          deps:['angular'],
          'exports':'angular.mock'
        }
    },

    // ask Require.js to load these files (all our tests)
    deps: tests,

    // start test run, once Require.js is done
    callback: window.__karma__.start
});
