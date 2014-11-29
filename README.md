#  shamir

Presentation slides about 3 articles from Adi Shamir: visual cryptography, secret
sharing and zero knowledge proofs.

### the presentation

the presentation is about three cryptographic articles Adi Shamir has written.  The audiance
is not expected to have any cryptographic knowledge before attending the presentation.  The
three articles are absolutly not releated one with each other.  The three subjects are
*  visual cryptography
*  secret sharing
*  zero knowledge proofs

### technicalities

The presentation is made with the [ipython notebook](http://ipython.org/notebook.html) using
[numpy](http://www.numpy.org/) and [matplotlib](http://matplotlib.org/).  The presentation
itself is rendered using [reveal.js](http://lab.hakim.se/reveal-js/).


#### stating the presentation

`make serve` should work!  Then you will need to browse to
http://localhost:2000/cryptographie_visuelle.slides.html to see the presentation
in a web browser.

#### hacking the presentation

`make env` should allow you to set up your dev environment on mac and linux.  Note
that you will need python 3, pip, virtualenv and all the binaries required to
`pip install` numpy and matplotlib.


