Notes for installation on Red-Hat based systems.

    # useradd pyuser
    # yum install python3-devel python27-virtualenv make gcc-c++
    # cp deploy/cgconfig.conf /etc/
    # cp deploy/tictactoe.ngx /etc/nginx/sites-enabled/
    # systemctl restart cgconfig.service
