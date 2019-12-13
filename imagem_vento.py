import numpy as np
from itertools import repeat
import datetime
import urllib.request, json

# Function to rotate a matrix
def rotateMatrix(mat):

    if not len(mat):
        return

    """
        top : starting row index
        bottom : ending row index
        left : starting column index
        right : ending column index
    """

    top = 0
    bottom = len(mat)-1

    left = 0
    right = len(mat[0])-1

    while left < right and top < bottom:

        # Store the first element of next row,
        # this element will replace first element of
        # current row
        prev = mat[top+1][left]

        # Move elements of top row one step right
        for i in range(left, right+1):
            curr = mat[top][i]
            mat[top][i] = prev
            prev = curr

        top += 1

        # Move elements of rightmost column one step downwards
        for i in range(top, bottom+1):
            curr = mat[i][right]
            mat[i][right] = prev
            prev = curr

        right -= 1

        # Move elements of bottom row one step left
        for i in range(right, left-1, -1):
            curr = mat[bottom][i]
            mat[bottom][i] = prev
            prev = curr

        bottom -= 1

        # Move elements of leftmost column one step upwards
        for i in range(bottom, top-1, -1):
            curr = mat[i][left]
            mat[i][left] = prev
            prev = curr

        left += 1

    return mat

def RodarMatrizN(matriz,n):

    for i in repeat(None, n):
        matriz = rotateMatrix(matriz)

    return matriz

def projeta_api_dirv(LAT,LONG,DIAS,ANGULO):


    dt_hoje = datetime.datetime.now() + datetime.timedelta(days=DIAS)
    dt_hoje = dt_hoje.replace(hour=0,minute=0,second=0,microsecond=0)


    api_1 = "https://projeta.cptec.inpe.br/api/v1/public/ETA/1/DAILY/2/12/2019/12/2019/D10M/" + LAT + "/" + LONG + "/"

    with urllib.request.urlopen(api_1) as url:
        data_1 = json.loads(url.read().decode())

    data = data_1

    for item in data:
        if datetime.datetime.strptime(item['date'], '%Y-%m-%d') == dt_hoje:
            ANGULO = item['value']

    return ANGULO

def Criar_Matriz(ang_rad,tamanho,matriz,tipo):
    vetor = 0
    sinal = 0
    if tipo == 'X':
        vetor = np.sqrt(abs(np.cos(np.deg2rad(ang_rad))))
        sinal = np.sign(np.cos(np.deg2rad(ang_rad)))
    if tipo == 'Y':
        sinal = np.sign(np.sin(np.deg2rad(ang_rad)))
        vetor = np.sqrt(abs(np.sin(np.deg2rad(ang_rad))))
    line = np.linspace(vetor,0,tamanho)
    matriz = np.outer(line,line)
    matriz = matriz*sinal
    return matriz

qse = projeta_api_dirv('-13.30','-46.18',0,0)
qsd = projeta_api_dirv('-13.30','-45.90',0,0)
qie = projeta_api_dirv('-13.46','-46.18',0,0)
qid = projeta_api_dirv('-13.46','-45.90',0,0)

"""
qse = 107
qsd = 110
qie = 105
qid = 108
"""

mesh_size = 100

"""
mat_qse_X = Criar_Matriz(qse,mesh_size,[],'X')
mat_qsd_X = RodarMatrizN(Criar_Matriz(qsd,mesh_size,[],'X'),((mesh_size - 1)*1))
mat_qid_X = RodarMatrizN(Criar_Matriz(qid,mesh_size,[],'X'),((mesh_size - 1)*2))
mat_qie_X = RodarMatrizN(Criar_Matriz(qie,mesh_size,[],'X'),((mesh_size - 1)*3))
"""
mat_qse_X = RodarMatrizN(Criar_Matriz(qse,mesh_size,[],'X'),((mesh_size - 1)*0))
mat_qsd_X = RodarMatrizN(Criar_Matriz(qsd,mesh_size,[],'X'),((mesh_size - 1)*1))
mat_qid_X = RodarMatrizN(Criar_Matriz(qid,mesh_size,[],'X'),((mesh_size - 1)*2))
mat_qie_X = RodarMatrizN(Criar_Matriz(qie,mesh_size,[],'X'),((mesh_size - 1)*3))

interpol_X = mat_qid_X + mat_qsd_X + mat_qse_X + mat_qie_X

mat_qse_Y = RodarMatrizN(Criar_Matriz(qse,mesh_size,[],'Y'),((mesh_size - 1)*0))
mat_qsd_Y = RodarMatrizN(Criar_Matriz(qsd,mesh_size,[],'Y'),((mesh_size - 1)*1))
mat_qid_Y = RodarMatrizN(Criar_Matriz(qid,mesh_size,[],'Y'),((mesh_size - 1)*2))
mat_qie_Y = RodarMatrizN(Criar_Matriz(qie,mesh_size,[],'Y'),((mesh_size - 1)*3))

interpol_Y = mat_qid_Y + mat_qsd_Y + mat_qse_Y + mat_qie_Y

interpol_Y_flip = np.flip(interpol_Y,0)


"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""

import tqdm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from matplotlib.collections import LineCollection

class Streamlines(object):
    """
    Copyright (c) 2011 Raymond Speth.
    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
    See: http://web.mit.edu/speth/Public/streamlines.py
    """

    def __init__(self, X, Y, U, V, res=0.125,
                 spacing=2, maxLen=2500, detectLoops=False):
        """
        Compute a set of streamlines covering the given velocity field.
        X and Y - 1D or 2D (e.g. generated by np.meshgrid) arrays of the
                  grid points. The mesh spacing is assumed to be uniform
                  in each dimension.
        U and V - 2D arrays of the velocity field.
        res - Sets the distance between successive points in each
              streamline (same units as X and Y)
        spacing - Sets the minimum density of streamlines, in grid points.
        maxLen - The maximum length of an individual streamline segment.
        detectLoops - Determines whether an attempt is made to stop extending
                      a given streamline before reaching maxLen points if
                      it forms a closed loop or reaches a velocity node.
        Plots are generated with the 'plot' or 'plotArrows' methods.
        """

        self.spacing = spacing
        self.detectLoops = detectLoops
        self.maxLen = maxLen
        self.res = res

        xa = np.asanyarray(X)
        ya = np.asanyarray(Y)
        self.x = xa if xa.ndim == 1 else xa[0]
        self.y = ya if ya.ndim == 1 else ya[:,0]
        self.u = U
        self.v = V
        self.dx = (self.x[-1]-self.x[0])/(self.x.size-1) # assume a regular grid
        self.dy = (self.y[-1]-self.y[0])/(self.y.size-1) # assume a regular grid
        self.dr = self.res * np.sqrt(self.dx * self.dy)

        # marker for which regions have contours
        self.used = np.zeros(self.u.shape, dtype=bool)
        self.used[0] = True
        self.used[-1] = True
        self.used[:,0] = True
        self.used[:,-1] = True

        # Don't try to compute streamlines in regions where there is no velocity data
        for i in range(self.x.size):
            for j in range(self.y.size):
                if self.u[j,i] == 0.0 and self.v[j,i] == 0.0:
                    self.used[j,i] = True

        # Make the streamlines
        self.streamlines = []
        while not self.used.all():
            nz = np.transpose(np.logical_not(self.used).nonzero())
            # Make a streamline starting at the first unrepresented grid point
            self.streamlines.append(self._makeStreamline(self.x[nz[0][1]],
                                                         self.y[nz[0][0]]))


    def _interp(self, x, y):
        """ Compute the velocity at point (x,y) """
        i = (x-self.x[0])/self.dx
        ai = i % 1

        j = (y-self.y[0])/self.dy
        aj = j % 1

        i, j = int(i), int(j)

        # Bilinear interpolation
        u = (self.u[j,i]*(1-ai)*(1-aj) +
             self.u[j,i+1]*ai*(1-aj) +
             self.u[j+1,i]*(1-ai)*aj +
             self.u[j+1,i+1]*ai*aj)

        v = (self.v[j,i]*(1-ai)*(1-aj) +
             self.v[j,i+1]*ai*(1-aj) +
             self.v[j+1,i]*(1-ai)*aj +
             self.v[j+1,i+1]*ai*aj)

        self.used[j:j+self.spacing,i:i+self.spacing] = True

        return u,v

    def _makeStreamline(self, x0, y0):
        """
        Compute a streamline extending in both directions from the given point.
        """

        sx, sy = self._makeHalfStreamline(x0, y0, 1) # forwards
        rx, ry = self._makeHalfStreamline(x0, y0, -1) # backwards

        rx.reverse()
        ry.reverse()

        return rx+[x0]+sx, ry+[y0]+sy

    def _makeHalfStreamline(self, x0, y0, sign):
        """
        Compute a streamline extending in one direction from the given point.
        """

        xmin = self.x[0]
        xmax = self.x[-1]
        ymin = self.y[0]
        ymax = self.y[-1]

        sx = []
        sy = []

        x = x0
        y = y0
        i = 0
        while xmin < x < xmax and ymin < y < ymax:
            u, v = self._interp(x, y)
            theta = np.arctan2(v,u)

            x += sign * self.dr * np.cos(theta)
            y += sign * self.dr * np.sin(theta)
            sx.append(x)
            sy.append(y)

            i += 1

            if self.detectLoops and i % 10 == 0 and self._detectLoop(sx, sy):
                break

            if i > self.maxLen / 2:
                break

        return sx, sy

    def _detectLoop(self, xVals, yVals):
        """ Detect closed loops and nodes in a streamline. """
        x = xVals[-1]
        y = yVals[-1]
        D = np.array([np.hypot(x-xj, y-yj)
                      for xj,yj in zip(xVals[:-1],yVals[:-1])])
        return (D < 0.9 * self.dr).any()


Y, X = np.mgrid[-3:3:100j, -3:3:100j]
"""U, V = -1 - X**2 + Y, 1 + X - X*Y**3"""

U =  -interpol_X
V = -interpol_Y_flip

"""speed = np.sqrt(U*U + V*V)
speed = K"""

fig = plt.figure(figsize=(4,4))
ax = plt.subplot(1, 1, 1, aspect=1)


lengths = []
colors = []
lines = []

s = Streamlines(X, Y, U, V)
for streamline in s.streamlines:
    x, y = streamline
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    n = len(segments)

    D = np.sqrt(((points[1:] - points[:-1])**2).sum(axis=-1))
    L = D.cumsum().reshape(n,1) + np.random.uniform(0,1)
    C = np.zeros((n,3))
    C[:] = (L*1.5) % 1

    #linewidths = np.zeros(n)
    #linewidths[:] = 1.5 - ((L.reshape(n)*1.5) % 1)

    # line = LineCollection(segments, color=colors, linewidth=linewidths)
    line = LineCollection(segments, color=C, linewidth=0.5)
    lengths.append(L)
    colors.append(C)
    lines.append(line)

    ax.add_collection(line)

def update(frame_no):
    for i in range(len(lines)):
        lengths[i] += 0.05
        colors[i][:] = (lengths[i]*1.5) % 1
        lines[i].set_color(colors[i])
    pbar.update()

ax.set_xlim(-3,+3), ax.set_xticks([])
ax.set_ylim(-3,+3), ax.set_yticks([])
plt.tight_layout()

n = 27
# animation = FuncAnimation(fig, update, interval=10)
animation = FuncAnimation(fig, update, frames=n, interval=20)
pbar = tqdm.tqdm(total=n)
# animation.save('wind.mp4', writer='ffmpeg', fps=60)
animation.save('wind.gif', writer='imagemagick', fps=30)
pbar.close()
plt.show()