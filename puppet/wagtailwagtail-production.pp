# vim:ts=4 sw=4 et:
class wagtail::site::production::wagtailiowagtail inherits wagtail::site::production {
    wagtail::app { 'wagtailiowagtail':
        ip               => $ipaddress,
        ip6              => $ipaddress6,
        manage_ip        => false,
        manage_db        => true,
        manage_user      => true,
        manage_settings  => false,
        settings         => 'wagtailio/settings',
        wsgi_module      => 'wagtailio.wsgi',
        requirements     => 'requirements.txt',
        servername       => 'wagtailio-production.torchboxapps.com',
        alias_redirect   => false,
        codebase_project => 'wagtailio',
        codebase_repo    => 'wagtailio',
        git_uri          => 'CODEBASE',
        django_version   => '1.7',
        staticdir        => "static",
        mediadir         => "media",
        deploy           => [ '@admin', '@wagtail', 'tomt', 'tom', 'karl', 'danb', 'chrisr', 'david' ],
        python_version   => '3.4',
        pg_version       => '9.4',
        manage_daemons   => [
            'celery worker -C -c1 -A wagtailio',
            'celery beat -A wagtailio -C -s $TMPDIR/celerybeat.db --pidfile=',
        ],
        admins           => {
            'Tom Dyson' => 'tom@torchbox.com',
            'Chris Rogers' => 'chris.rogers@torchbox.com',
            'Dan Braghis' => 'dan.braghis@torchbox.com',
            'Dave Cranwell' => 'david@torchbox.com',
            'Karl Hobley' => 'karl.hobley@torchbox.com'
        },
        nagios_url       => '/',
        auth => {
            enabled       => true,
            hosts         => [ 'tbx' ],
            users         => {
                'wagtailio'  => 'newwagtailio',
            },
        },
    }
}
