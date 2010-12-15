include arch.make

# urwid
URW_URL=https://github.com/wardi/urwid/tarball/master
URW_TGZ=urwid.tgz

# pyopengl
PGL_URL=http://sourceforge.net/projects/pyopengl/files/PyOpenGL/3.0.1/PyOpenGL-3.0.1.tar.gz/download
PGL_TGZ=pyopengl.tgz

# matplotlib
MPL_URL=http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.0/matplotlib-1.0.0.tar.gz/download
MPL_TGZ=matplotlib.tgz

.PHONY: all urwid pyopengl matplotlib

all: urwid pyopengl matplotlib

urwid:
	if ! test -d ./urwid.git;then \
	  if ! test -f $(URW_TGZ);then \
	    $(DL) -O $(URW_TGZ) $(URW_URL);fi; \
	  $(TAR) xvzf $(URW_TGZ); \
	  mv ./*urwid-* ./urwid.git; \
	  ln -s ./urwid.git/urwid ./urwid; fi;

pyopengl:
	if ! test -d ./OpenGL;then \
	  if ! test -f $(PGL_TGZ);then \
	    $(DL) -O $(PGL_TGZ) $(PGL_URL);fi; \
	  $(TAR) xvzf $(PGL_TGZ); \
	  mv ./PyOpenGL-* ./PyOpenGL.src; \
	  ln -s ./PyOpenGL.src/OpenGL ./OpenGL; fi;

matplotlib:
	if ! test -d ./matplotlib;then \
	  if ! test -f $(MPL_TGZ);then \
	    $(DL) -O $(MPL_TGZ) $(MPL_URL);fi; \
	  $(TAR) xvzf $(MPL_TGZ); \
	  mv ./matplotlib-* ./matplotlib.src; \
	  mv ./matplotlib.src/__init__.py ./matplotlib.src/__init__.py.bak; \
	  ln -s ./matplotlib.src/lib/matplotlib ./matplotlib; \
	  ln -s ./matplotlib.src/lib/mpl_toolkits ./mpl_toolkits; \
	  fi;


clean:
	rm -fR ./urwid.git
	rm -fR ./PyOpenGL.src
	rm -fR ./matplotlib.src
	rm *.tar.gz *.tgz urwid OpenGL matplotlib mpl_toolkits

