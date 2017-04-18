# HTTP-PROXY

## What is it? And why use it?

Sometimes a service can still be under heavy development. At that point, simultaneously developing a charm can be quite difficult. However, you want to be able to connect the HTTP interface of your service to other already charmed services in your model. This proxy charm will make this possible.

You can also use this proxy charm to connect services inside your model to an external http endpoint.

## How to use

Deploy e.g. the ssl-termination-proxy

    juju deploy cs:~tengu-team/ssl-termination-proxy

Deploy the http-proxy charm

    juju deploy cs:~tengu-team/http-proxy

Add relation between the ssl-termination-proxy and the http-proxy

    juju add-relation ssl-termination-proxy http-proxy

Check the deployment status (press <kbd>ctrl</kbd>-<kbd>c</kbd> to exit)

    watch -c juju status --color

When the deployment is done ('active', 'Ready'), your http endpoint should now be https enabled

# Contact Information

## Authors

This software was created in the [IDLab research group](https://www.ugent.be/ea/idlab) of [Ghent University](https://www.ugent.be) in Belgium. This software is used in [Tengu](https://tengu.io), a project that aims to make experimenting with data frameworks and tools as easy as possible.

 - Gregory Van Seghbroeck <gregory.vanseghbroeck@ugent.be>
