# vim:ts=4 sw=4 et:
class wagtail::site::staging::wagtailiowagtail inherits wagtail::site::staging {
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
        servername       => 'wagtailio-staging.torchboxapps.com',
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
        manade_daemons   => [
            'celery worker -C -c1 -A wagtailio',
            'celery beat -A wagtailio -C -s $TMPDIR/celerybeat.db --pidfile=',
        ],
        admins           => {
            # CHANGEME
            # List of users to send error emails to. Eg:
            # 'Joe Bloggs' => 'joe.bloggs@torchbox.com',
        },
        nagios_url       => '/',
        auth => {
            enabled       => true,
            hosts         => [ 'tbx' ],
            users         => {
                # CHANGEME
                # This is the credentials for HTTP authentication. Eg:
                # 'username'  => 'password',
            },
        },
    }
}
