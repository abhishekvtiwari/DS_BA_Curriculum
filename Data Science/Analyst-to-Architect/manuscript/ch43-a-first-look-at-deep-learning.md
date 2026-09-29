# Chapter 43. A First Look at Deep Learning

*Part 4 — Machine Learning & Data Science*

> **Chapter at a glance**
>
> **You will learn to:** install PyTorch and use its tensors · compute a single neuron by hand and recognize it as logistic regression in disguise · explain why one neuron can't solve every problem, and watch a network fail and then succeed on a real example · compute a full forward pass through a small network by hand and match it in PyTorch · work one backward pass by hand with the chain rule, and check it against PyTorch's automatic gradients and a hand-nudged gradient · train a small neural network on tabular data and compare it honestly with logistic regression and gradient boosting · understand what a convolution does, and train a small image classifier · walk through transfer learning end to end, and see when it helps and when it doesn't.
>
> **Before you start:** Chapter 35 (vectors, matrix products, derivatives and gradients, gradient descent, log loss), Chapter 36 (splits, scikit-learn, pipelines), Chapter 37 (logistic regression and the sigmoid, gradient boosting, bias and variance), Chapter 29 (classes, section 29.5), Chapter 39 (AUC, and why accuracy misleads on imbalanced data), Chapter 41 (softmax, and word embeddings as a preview of learned representations).
>
> **Time needed:** 12–15 hours over two weeks, in three sittings: sections 43.0–43.4 (PyTorch, neurons, and the backward pass by hand), about 5 hours; sections 43.5–43.6 (a network on tables, and one on images), about 4 hours; section 43.7 and the project, about 4 hours, plus the exercises. Everything runs on an ordinary laptop's CPU in a few minutes; no GPU is needed.
>
> **Tools:** Python 3 with scikit-learn (installed in Chapter 35) and PyTorch, installed in section 43.0 (both free).
>
> **Practice data:** Riverstone's customer accounts (Chapter 37, for the tabular network) and scikit-learn's built-in handwritten-digit images (1,797 small images, no download needed, for the image classifier and transfer learning). Every number in this chapter was calculated, and every output shown is real.

---

## Why this matters

Deep learning gets credited with everything from language models to self-driving cars, and that reputation makes it tempting to reach for a neural network on every problem. This chapter's honest position, backed by its own numbers, is narrower and more useful: **a neural network is a flexible way to stack the ideas from Chapters 35 and 37 into deeper, more expressive models**, and it earns its complexity on some problems (images, text, audio, huge datasets) and not on others (Riverstone's tabular churn data, where gradient boosting still wins).

Three things you'll be able to do by the end:

- Explain what a neural network actually computes, without hand-waving, because you'll have done the arithmetic yourself.
- Train one in PyTorch, on a table of numbers and on a set of images, and evaluate it the same honest way Chapters 37 and 39 taught.
- Answer the interview question "when would you use deep learning instead of gradient boosting?" with a real comparison behind you, not a guess.

---

## In plain English

**Think back to Chapter 37's logistic regression: a weighted sum of features, squeezed through a sigmoid, giving a probability.** That whole calculation is what people call a **neuron**. One neuron is exactly one logistic regression.

A **layer** is a group of neurons, each looking at the same inputs and computing its own weighted sum. A **network** stacks layers: the outputs of one layer become the inputs to the next. Stacking matters because a single neuron can only draw one straight-line boundary through the data, and some real patterns need more than a straight line, no matter how you tilt it.

**Training** a network is exactly Chapter 35's gradient descent, applied to many more parameters at once. The one new piece of machinery is **backpropagation**: an efficient way to compute the gradient of every parameter in every layer, using a rule from calculus called the **chain rule**. The library applies it automatically, so in practice you never do it by hand. This chapter has you do it by hand *once*, on a tiny example (section 43.4), purely so the automation stops feeling like magic.

---

## 43.0 Setting up

### Installing PyTorch

This chapter needs one library that no earlier chapter installed. **PyTorch** is a free, open-source library for building and training neural networks. Open a terminal, go to the book's `companion` folder, make a folder for this chapter's notebook, and activate your virtual environment (Chapter 17, section 17.0; terminal basics are in Chapter 26, section 26.0).

On **Windows** or **macOS**, install it the usual way:

```bash
python -m pip install torch
```

On **Linux**, or Windows with WSL, add one setting that asks for the CPU-only version:

```bash
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Then record it, as in Chapter 35, section 35.9:

```bash
python -m pip freeze > requirements.txt
```

- `python -m pip install torch` downloads PyTorch into your active environment, as for every library since Chapter 18.
- **Why Linux is different.** On Linux, the standard download is the version that can use an NVIDIA graphics card (a **GPU**), and it brings several gigabytes of NVIDIA libraries with it. `--index-url https://download.pytorch.org/whl/cpu` tells pip to fetch PyTorch from PyTorch's own download server, from its folder of CPU-only builds, which are much smaller. The Windows and macOS downloads are already CPU-only. Everything in this chapter runs on a CPU.
- `python -m pip freeze > requirements.txt` rewrites the list of installed packages, so `torch` is recorded.

Start Jupyter from your chapter folder (`companion/ch43/`), open a new notebook, and run every cell in this chapter in order: each uses names made by the cells before it.

### Checking the install

```python
import torch

print(torch.__version__)
print("GPU available:", torch.cuda.is_available())
```

```
2.14.0+cu130
GPU available: False
```

- `import torch` loads PyTorch. The library's name on disk is `torch`, not `pytorch`. If this line fails with `ModuleNotFoundError`, the notebook is using a different environment from the one you installed into (Chapter 17, section 17.0).
- `torch.__version__` is the version. The part after the `+` names the build: this book's outputs came from a build that includes GPU support (`cu130` means CUDA 13.0, NVIDIA's GPU toolkit); yours may end in `+cpu`, or have no `+` at all. The number before the `+` is what matters.
- `torch.cuda.is_available()` asks whether PyTorch can use an NVIDIA GPU here. **`False` is expected and fine**: every model in this chapter trains on the CPU in seconds.

### Your first tensor

PyTorch's basic object is the **tensor**: a grid of numbers, like the NumPy arrays of Chapter 18 (section 18.1), that can also keep track of how it was computed, so PyTorch can work out gradients later (section 43.4). Make one from Sharma Hardware's two numbers from Chapter 35 (16 orders, ₹5.03 lakh revenue):

```python
sharma = torch.tensor([16.0, 5.03])
print(sharma)
print(sharma.shape, sharma.dtype)
print(sharma * 2)
print(sharma.tolist())
```

```
tensor([16.0000,  5.0300])
torch.Size([2]) torch.float32
tensor([32.0000, 10.0600])
[16.0, 5.03000020980835]
```

- `torch.tensor([16.0, 5.03])` builds a tensor from a Python list, the way `np.array` builds an array.
- `.shape` is `torch.Size([2])`: one dimension with two numbers, like an array's shape.
- `.dtype` is the number type. **`torch.float32`** stores each number in 32 bits, which keeps about 7 significant digits. NumPy and pandas use `float64` (Chapter 18), with about 16. Neural networks use 32 bits because they're twice as compact and faster, and the lost digits don't matter for training.
- `sharma * 2` multiplies every number at once, as with a NumPy array.
- `.tolist()` turns the tensor back into a plain Python list, and shows the price of 32 bits: 5.03 can't be stored exactly, so the nearest 32-bit number, 5.03000020980835, comes back. The difference is in the eighth digit. You'll see tails like this in PyTorch outputs; they're rounding, not mistakes.

---

## 43.1 A neuron is logistic regression

A neuron takes a row of features, computes a weighted sum plus a bias, *z* = *w* · *x* + *b* (Chapter 35's dot product), and passes *z* through a function. With the sigmoid, that's Chapter 37's logistic regression (section 37.3). Here it is for Sharma Hardware's vector, in NumPy:

```python
import math

import numpy as np

x = np.array([16, 5.03])  # Sharma Hardware: 16 orders, ₹5.03 lakh revenue (Chapter 35)
w = np.array([0.05, 0.9])  # made-up weights, for illustration only
b = -1.2

z = w @ x + b
a = 1 / (1 + math.exp(-z))
print(f"z = w . x + b = {w[0]} x {x[0]} + {w[1]} x {x[1]} + ({b}) = {z:.3f}")
print(f"sigmoid(z) = {a:.3f}")
```

```
z = w . x + b = 0.05 x 16.0 + 0.9 x 5.03 + (-1.2) = 4.127
sigmoid(z) = 0.984
```

- `w @ x` is the dot product (Chapter 35, section 35.2): 0.05 × 16 + 0.9 × 5.03 = 0.8 + 4.527 = 5.327. Adding the bias, −1.2, gives *z* = 4.127.
- `1 / (1 + math.exp(-z))` is the sigmoid from Chapter 37: it squeezes *z* into the range 0 to 1.
- The weights are invented to show the arithmetic. They weren't learned from data, so 0.984 is **not** a real prediction about Sharma Hardware.

**Reading it.** Nothing here is new. A neuron computes a weighted sum plus a bias, then applies an **activation function**, here the sigmoid, to turn the result into something useful (a probability). Chapter 37's logistic regression *is* a single neuron with a sigmoid activation; deep learning starts by giving that neuron company.

### Two more activation functions: ReLU and tanh

Networks use other activation functions too. Two matter in this chapter:

- **ReLU** (rectified linear unit) passes positive values through unchanged and turns negative ones into 0. Modern networks mostly use it in their hidden layers (section 43.2).
- **tanh** (said "tan-h", the hyperbolic tangent) is an S-curve like the sigmoid, but it runs from −1 to 1 and is centred on 0. Python has it built in as `math.tanh`.

Before you run the next cell, predict: what does ReLU give for −2, and for 3?

```python
def relu(z):
    return max(0.0, z)


for z in [-2, -0.1, 0, 0.5, 3]:
    sig = 1 / (1 + math.exp(-z))
    print(f"z = {z:>4}   relu {relu(z):>4}   sigmoid {sig:.3f}   tanh {math.tanh(z):>6.3f}")
```

```
z =   -2   relu  0.0   sigmoid 0.119   tanh -0.964
z = -0.1   relu  0.0   sigmoid 0.475   tanh -0.100
z =    0   relu  0.0   sigmoid 0.500   tanh  0.000
z =  0.5   relu  0.5   sigmoid 0.622   tanh  0.462
z =    3   relu    3   sigmoid 0.953   tanh  0.995
```

- `max(0.0, z)` is the whole of ReLU: the larger of 0 and *z*. `max` returns whichever argument wins, so `relu(3)` prints the whole number `3` and `relu(-2)` prints `0.0`.
- `{z:>4}` right-aligns *z* in 4 characters, and `{math.tanh(z):>6.3f}` right-aligns tanh with 3 decimals, so the columns line up.
- The sigmoid stays between 0 and 1 and gives 0.5 at *z* = 0; tanh stays between −1 and 1 and gives 0 at *z* = 0.

### Why the slope of the activation matters

Chapter 35 used "gradient" for the slope of the loss. Training a network also needs the **slope of each activation function**: how much its output moves when its input moves a little. The sigmoid's slope has a simple formula, sigmoid(*z*) × (1 − sigmoid(*z*)); ReLU's slope is 1 for positive *z* and 0 for negative *z*. Compare them:

```python
for z in [-2, 0, 3]:
    s = 1 / (1 + math.exp(-z))
    relu_slope = 1 if z > 0 else 0
    print(f"z = {z:>2}   sigmoid slope {s * (1 - s):.3f}   relu slope {relu_slope}")
print(f"ten sigmoid slopes of 0.25 multiplied together: {0.25**10:.7f}")
```

```
z = -2   sigmoid slope 0.105   relu slope 0
z =  0   sigmoid slope 0.250   relu slope 0
z =  3   sigmoid slope 0.045   relu slope 1
ten sigmoid slopes of 0.25 multiplied together: 0.0000010
```

- `s * (1 - s)` is the sigmoid's slope at *z*. It's largest, 0.25, at *z* = 0, and small far from 0: the curve is almost flat there.
- `1 if z > 0 else 0` is ReLU's slope, written on one line: 1 when *z* is positive, otherwise 0.
- `0.25**10` multiplies ten slopes of 0.25 together.

**Reading it.** Section 43.4 shows that training multiplies the slopes of every layer the signal passes through. With sigmoid in ten stacked layers, even the *best* case multiplies ten slopes of 0.25, about one millionth, so the early layers get almost no signal and barely learn. That's the **vanishing gradient**. ReLU's slope is exactly 1 for positive inputs, so nothing shrinks, which is why hidden layers mostly use ReLU. The sigmoid is still used at a network's *output*, where you want a 0–1 probability.

---
## 43.2 Why one neuron isn't enough

### XOR: a pattern no straight line can separate

A single neuron draws one straight decision boundary: on one side it predicts above 0.5, on the other below. Some patterns can't be separated by any straight line, however you set the weights. The classic example is **XOR** ("exclusive or"): *true if exactly one of two conditions holds*. Put the four possible cases into tensors:

```python
torch.manual_seed(43)

X_xor = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
y_xor = torch.tensor([[0.0], [1.0], [1.0], [0.0]])
print("XOR: a customer gets a discount if exactly one of two conditions holds")
for row, target in zip(X_xor.tolist(), y_xor.tolist()):
    print(f"  inputs {row} -> target {target[0]:.0f}")
```

```
XOR: a customer gets a discount if exactly one of two conditions holds
  inputs [0.0, 0.0] -> target 0
  inputs [0.0, 1.0] -> target 1
  inputs [1.0, 0.0] -> target 1
  inputs [1.0, 1.0] -> target 0
```

- `torch.manual_seed(43)` fixes PyTorch's random number generator, like `random_state=37` in scikit-learn (Chapter 36). A new network starts with random weights; with the seed set, you get exactly the weights, and the outputs, shown in this chapter. Each training cell below sets it again.
- `X_xor` is a 4 × 2 tensor: four rows, two inputs each. `y_xor` is 4 × 1: one target per row, kept as a column because the network will output a column.
- `zip(X_xor.tolist(), y_xor.tolist())` pairs each row of inputs with its target, as `zip` does with two lists (Chapter 17); `target[0]` takes the one number out of each one-item target list.

![Left panel: the four XOR points on a square, 0 at bottom-left and top-right, 1 at top-left and bottom-right, with a dashed straight line that leaves a 1 on the same side as a 0. Right panel: the same four points over the two-layer network's learned regions, a diagonal band predicted 1 between two regions predicted 0](figures/fig43-1-xor.svg)

*Figure 43.1 — XOR. Left: any straight line leaves a 1 and a 0 on the same side. Right: the network with one hidden layer (end of this section) learns a bent boundary: a band for 1, with 0 on both sides.*

Look at Figure 43.1's left panel and try to draw one straight line that puts the two 1s on one side and the two 0s on the other. It can't be done: the 1s sit on one diagonal and the 0s on the other. Now train a single neuron on it anyway, one piece at a time.

### A single neuron in PyTorch

First, build the neuron:

```python
import torch.nn as nn

single_neuron = nn.Sequential(nn.Linear(2, 1), nn.Sigmoid())
print(single_neuron)
layer = single_neuron[0]
print("weights:", layer.weight.tolist())
print("bias:   ", layer.bias.tolist())
```

```
Sequential(
  (0): Linear(in_features=2, out_features=1, bias=True)
  (1): Sigmoid()
)
weights: [[-0.06509867310523987, -0.42922618985176086]]
bias:    [0.5954343676567078]
```

- `torch.nn`, imported as `nn`, is PyTorch's toolbox of network pieces.
- **`nn.Linear(2, 1)`** is a layer that takes **2** inputs and produces **1** output: *z* = *w* · *x* + *b*. It holds 2 weights and 1 bias, the `w` and `b` of section 43.1.
- **`nn.Sigmoid()`** applies the sigmoid to whatever comes in.
- **`nn.Sequential(...)`** chains the pieces: apply them in order, the output of each feeding the next. So `single_neuron` computes sigmoid(*w* · *x* + *b*): logistic regression.
- `single_neuron[0]` is the first piece, the `Linear` layer; `.weight` and `.bias` are its numbers. They start **random** (that's what `manual_seed` fixed), and training will change them.

Second, one **forward pass**: feed all four rows through the neuron.

```python
prediction = single_neuron(X_xor)
print(prediction)
```

```
tensor([[0.6446],
        [0.5415],
        [0.6296],
        [0.5253]], grad_fn=<SigmoidBackward0>)
```

- `single_neuron(X_xor)` runs every row through `Linear` and then `Sigmoid`, and returns a 4 × 1 tensor: one probability per row. With random weights they're meaningless so far.
- `grad_fn=<SigmoidBackward0>` is PyTorch remembering that the last step was a sigmoid. It keeps this record of every step, so it can work backwards through them to find gradients (section 43.4).

Third, the loss. **`nn.BCELoss`** is binary cross-entropy, which is Chapter 35's **log loss** (section 35.9) under its other name:

```python
from sklearn.metrics import log_loss

loss_fn = nn.BCELoss()
loss = loss_fn(prediction, y_xor)
print(f"BCELoss:           {loss.item():.4f}")
print(f"sklearn log_loss:  {log_loss(y_xor.ravel(), prediction.detach().ravel()):.4f}")
```

```
BCELoss:           0.7139
sklearn log_loss:  0.7139
```

- `nn.BCELoss()` makes the loss function; `loss_fn(prediction, y_xor)` computes the average log loss of the four predictions against the four targets.
- **`.item()`** takes the single number out of a one-number tensor, as a plain Python number you can format.
- For the check with scikit-learn's `log_loss` (Chapter 36), `.ravel()` flattens each 4 × 1 column into four numbers, as in NumPy. **`.detach()`** hands over the predictions without PyTorch's gradient record; other libraries can't read a tensor that is still keeping one.

The two agree. The loss is Chapter 35's log loss; nothing new.

Fourth, one **training step**, Chapter 35's gradient descent. Watch the weights before and after:

```python
optimizer = torch.optim.SGD(single_neuron.parameters(), lr=0.5)
print("before:  ", layer.weight.tolist())
optimizer.zero_grad()
loss.backward()
print("gradient:", layer.weight.grad.tolist())
optimizer.step()
print("after:   ", layer.weight.tolist())
```

```
before:   [[-0.06509867310523987, -0.42922618985176086]]
gradient: [[0.03870430588722229, 0.01667812466621399]]
after:    [[-0.08445082604885101, -0.43756526708602905]]
```

- **`torch.optim.SGD`** is gradient descent. `single_neuron.parameters()` hands it every weight and bias to look after, and **`lr=0.5`** is the learning rate (Chapter 35, section 35.6), the size of each step.
- **`optimizer.zero_grad()`** clears any gradients left from a previous step. PyTorch *adds* new gradients to old ones, so forgetting this line makes training go wrong (see *Common mistakes*).
- **`loss.backward()`** computes the gradient of the loss with respect to every parameter and stores it in each parameter's `.grad`. This is backpropagation (section 43.4).
- **`optimizer.step()`** moves every parameter one step downhill: new weight = old weight − `lr` × gradient.

Check the first weight by hand: before − 0.5 × gradient gives the "after" value. That's the whole update rule, the same one you ran in NumPy in Chapter 35.

Now repeat those four lines (predict, loss, backward, step) 2,000 times:

```python
for step in range(2000):
    optimizer.zero_grad()
    prediction = single_neuron(X_xor)
    loss = loss_fn(prediction, y_xor)
    loss.backward()
    optimizer.step()

print(f"after 2000 more steps, loss = {loss.item():.4f}")
print("predictions:", prediction.detach().numpy().round(3).ravel())
print("targets:    ", y_xor.numpy().ravel())
```

```
after 2000 more steps, loss = 0.6931
predictions: [0.5 0.5 0.5 0.5]
targets:     [0. 1. 1. 0.]
```

- Each pass of the loop is one training step: clear old gradients, predict, measure the loss, compute gradients, step.
- `prediction.detach().numpy()` turns the tensor into a NumPy array (without the gradient record), so `.round(3)` and `.ravel()` work as in Chapter 18.

**Reading it.** After 2,000 more steps the loss has settled at 0.6931, which is *exactly* ln 2 (Chapter 35, section 35.8): the log loss of predicting 50% for every row. The single neuron learned nothing useful, because there is no straight line, and therefore no setting of its weights, that does better on these four points. For a single neuron on XOR, predicting 0.5 everywhere is the best it can possibly do. This isn't a training failure that more steps or a different learning rate would fix; it's a **structural limitation** of one neuron.

### Adding a hidden layer

Now put a **hidden layer** of 4 neurons between the inputs and the output. "Hidden" only means it's neither the input nor the output:

```python
torch.manual_seed(43)

two_layer = nn.Sequential(nn.Linear(2, 4), nn.Tanh(), nn.Linear(4, 1), nn.Sigmoid())
optimizer2 = torch.optim.SGD(two_layer.parameters(), lr=0.5)

for step in range(3000):
    optimizer2.zero_grad()
    prediction2 = two_layer(X_xor)
    loss2 = loss_fn(prediction2, y_xor)
    loss2.backward()
    optimizer2.step()

print(f"after 3000 steps, loss = {loss2.item():.5f}")
print("predictions:", prediction2.detach().numpy().round(3).ravel())
print(f"total parameters: {sum(p.numel() for p in two_layer.parameters())}")
```

```
after 3000 steps, loss = 0.00097
predictions: [0.001 0.999 0.999 0.001]
total parameters: 17
```

- **`nn.Linear(2, 4)`** turns the 2 inputs into 4 weighted sums, one per hidden neuron: 2 × 4 = 8 weights and 4 biases.
- **`nn.Tanh()`** applies tanh (section 43.1) to each of the 4.
- **`nn.Linear(4, 1)`** combines the 4 hidden outputs into one weighted sum: 4 weights and 1 bias. `nn.Sigmoid()` turns it into a probability.
- The training loop is the one above, with new names.
- `p.numel()` counts the numbers in one parameter tensor, and `sum(...)` adds them up: 8 + 4 + 4 + 1 = **17**.

Why tanh and not ReLU, which section 43.1 said hidden layers usually use? On a four-row toy problem with only four hidden neurons, a ReLU neuron whose weighted sum is negative for all four rows outputs 0 and has a slope of 0, so it stops learning for good (a "dead" neuron). With the same seed, swap in ReLU and see:

```python
torch.manual_seed(43)
relu_net = nn.Sequential(nn.Linear(2, 4), nn.ReLU(), nn.Linear(4, 1), nn.Sigmoid())
relu_optimizer = torch.optim.SGD(relu_net.parameters(), lr=0.5)
for step in range(3000):
    relu_optimizer.zero_grad()
    relu_loss = loss_fn(relu_net(X_xor), y_xor)
    relu_loss.backward()
    relu_optimizer.step()
print(f"ReLU hidden layer, after 3000 steps: loss = {relu_loss.item():.4f}")
```

```
ReLU hidden layer, after 3000 steps: loss = 0.3467
```

`nn.ReLU()` is the only change. The loss stops at 0.3467, well short of solving XOR: some of its four neurons died. With thousands of neurons and rows, a few dead ones don't matter, which is why ReLU works well in real networks; on this tiny problem, tanh is the safer choice.

**Reading it.** With a hidden layer of just 4 tanh neurons, the network solves XOR almost perfectly (predictions of 0.001, 0.999, 0.999, 0.001 against targets of 0, 1, 1, 0). Each hidden neuron draws its own straight line, and the output layer combines them into a shape a single line never could: the diagonal band in Figure 43.1's right panel. **This is the reason depth exists**: layers with nonlinear activations between them let a network represent patterns a single layer structurally cannot, no matter how it's trained.

---

## 43.3 A full forward pass, by hand

Take the smallest multi-layer network, 2 inputs, 2 hidden neurons (tanh), and 1 output (sigmoid), and push one example through it, in PyTorch and by hand, to see that nothing is hidden. Figure 43.2 shows the network with the weights we'll use.

![A network diagram: two input circles, x1 = 1.0 and x2 = 0.5, each connected to two hidden circles by arrows labelled with the weights 0.3, -0.2, 0.4 and 0.1; the hidden circles show z1 and a1 values 0.30 and 0.2913, and 0.35 and 0.3364; both connect to one output circle by weights 0.5 and -0.6, which shows z2 = 0.1438 and a2 = 0.5359](figures/fig43-2-network.svg)

*Figure 43.2 — The 2-2-1 network of sections 43.3 and 43.4. Each hidden neuron adds its bias (0.1 and −0.1) to its weighted sum, then applies tanh; the output neuron adds 0.2, then applies the sigmoid.*

```python
x_tiny = torch.tensor([1.0, 0.5])
W1 = torch.tensor([[0.3, -0.2], [0.4, 0.1]])  # 2 hidden units x 2 inputs
b1 = torch.tensor([0.1, -0.1])
W2 = torch.tensor([[0.5, -0.6]])  # 1 output x 2 hidden units
b2 = torch.tensor([0.2])

z1 = W1 @ x_tiny + b1
a1 = torch.tanh(z1)
z2 = W2 @ a1 + b2
a2 = torch.sigmoid(z2)

print(f"hidden layer:  z1 = {[round(v, 4) for v in z1.tolist()]}   a1 = {[round(v, 4) for v in a1.tolist()]}")
print(f"output layer:  z2 = {z2.item():.4f}   a2 = {a2.item():.4f}")
```

```
hidden layer:  z1 = [0.3, 0.35]   a1 = [0.2913, 0.3364]
output layer:  z2 = 0.1438   a2 = 0.5359
```

- `W1` holds one row of weights per hidden neuron; `W1 @ x_tiny` computes both hidden neurons' weighted sums in a single matrix product (Chapter 35, section 35.3), and `+ b1` adds each one's bias.
- `torch.tanh` and `torch.sigmoid` apply the activations to every number in a tensor.
- `W2` is 1 × 2: one output neuron with a weight for each hidden neuron.
- `[round(v, 4) for v in z1.tolist()]` rounds each number to 4 decimals. Without it, `z1` would print as `[0.30000001192092896, 0.3500000238418579]`: the 32-bit tails from section 43.0.

Now the same calculation by hand, with plain Python numbers:

```python
z1_0 = 0.3 * 1.0 + (-0.2) * 0.5 + 0.1
z1_1 = 0.4 * 1.0 + 0.1 * 0.5 + (-0.1)
a1_0, a1_1 = math.tanh(z1_0), math.tanh(z1_1)
z2_hand = 0.5 * a1_0 + (-0.6) * a1_1 + 0.2
a2_hand = 1 / (1 + math.exp(-z2_hand))
print(f"by hand: z1 = [{z1_0:.2f}, {z1_1:.2f}]   a1 = [{a1_0:.4f}, {a1_1:.4f}]")
print(f"by hand: z2 = {z2_hand:.4f}   a2 = {a2_hand:.4f}")
print("matches PyTorch to 9 decimal places:", abs(a2_hand - a2.item()) < 1e-9)
```

```
by hand: z1 = [0.30, 0.35]   a1 = [0.2913, 0.3364]
by hand: z2 = 0.1438   a2 = 0.5359
matches PyTorch to 9 decimal places: True
```

- `z1_0` is the first hidden neuron: 0.3 × 1.0 − 0.2 × 0.5 + 0.1 = 0.30. `z1_1` is the second: 0.4 × 1.0 + 0.1 × 0.5 − 0.1 = 0.35.
- `a1_0, a1_1 = ...` assigns two names at once (Chapter 17): tanh of each.
- `z2_hand` is the output neuron: 0.5 × 0.2913 − 0.6 × 0.3364 + 0.2 = 0.1438, and `a2_hand` its sigmoid.
- `abs(a2_hand - a2.item()) < 1e-9` checks that the two answers differ by less than one billionth. (`1e-9` is scientific notation for 0.000000001, Chapter 35.)

**Reading it.** Every number matches PyTorch's to the precision shown, because it's the same calculation. This is what **forward pass** means: multiply, add a bias, activate, and repeat for each layer, ending at the output.

---

## 43.4 Backpropagation: the chain rule, automated

Training needs the gradient of the loss with respect to *every* weight in *every* layer. **Backpropagation** computes it efficiently, starting at the loss and working backwards through the network, layer by layer, reusing each result for the layer before it. In PyTorch, `.backward()` is backpropagation, one line however many layers there are. PyTorch's name for this automatic gradient machinery is **autograd**.

Suppose this example's true label is 1. First let PyTorch compute the gradients, then do the same by hand, then check both with a nudge.

### Autograd's answer

```python
W1g = W1.clone().requires_grad_()
b1g = b1.clone().requires_grad_()
W2g = W2.clone().requires_grad_()
b2g = b2.clone().requires_grad_()
target_tiny = torch.tensor([1.0])


def tiny_forward(W1, b1, W2, b2, x):
    return torch.sigmoid(W2 @ torch.tanh(W1 @ x + b1) + b2)


loss_tiny = nn.functional.binary_cross_entropy(
    tiny_forward(W1g, b1g, W2g, b2g, x_tiny), target_tiny
)
loss_tiny.backward()
print(f"loss = {loss_tiny.item():.4f}")
print(f"autograd dL/dW2 = {[round(v, 4) for v in W2g.grad[0].tolist()]}")
print(f"autograd dL/dW1 = {[[round(v, 4) for v in row] for row in W1g.grad.tolist()]}")
```

```
loss = 0.6238
autograd dL/dW2 = [-0.1352, -0.1561]
autograd dL/dW1 = [[-0.2124, -0.1062], [0.247, 0.1235]]
```

- **`.clone()`** makes a copy, so the original `W1`, `b1`, `W2` and `b2` stay untouched for the checks below.
- **`.requires_grad_()`** tells PyTorch to track how this tensor affects anything computed from it, so that `backward()` can find its gradient. The weights inside `nn.Linear` have this switched on automatically; tensors you make yourself don't.
- `tiny_forward` is section 43.3's forward pass in one line: tanh of the hidden sums, then the sigmoid of the output sum.
- **`nn.functional.binary_cross_entropy`** is the function form of `nn.BCELoss`: the same log loss, called directly instead of made first.
- `loss_tiny.backward()` runs backpropagation, and **`.grad`** is where it leaves each gradient: `W2g.grad` has the same shape as `W2g`, one gradient per weight. `W2g.grad[0]` is its only row.
- `[[round(v, 4) for v in row] for row in ...]` rounds every number of the 2 × 2 grid: the outer part goes through the rows, the inner part through the numbers of each row.

The loss is −ln 0.5359 = 0.6238, Chapter 35's log loss for a true label of 1. Both gradients on `W2` are negative, so raising either weight would lower the loss.

### The backward pass by hand

You met the key idea in Chapter 35 (section 35.4), in "Where the slope formula comes from": the squared error reacted to the error, the error reacted to *w*, and the slope with respect to *w* was the two reactions multiplied together (2 × error × *x*). That multiplication has a name, the **chain rule**:

> If *a* changes *b*, and *b* changes *c*, then how much *a* changes *c* = (how much *a* changes *b*) × (how much *b* changes *c*).
>
> Example: if one more order adds ₹2,000 of revenue, and each ₹1,000 of revenue adds ₹150 of profit, then one more order adds 2 × ₹150 = ₹300 of profit.

A network is a chain: each weight changes a weighted sum, which changes an activation, which changes the next weighted sum, and so on to the loss. So a weight's gradient is the product of the slopes along its path. Work backwards from the loss, with the numbers from section 43.3 and the label *y* = 1.

**Step 1: the output neuron.** For a sigmoid followed by log loss, the chain rule gives a very short answer. The slope of −ln *a*₂ with respect to *a*₂ is −1 ÷ *a*₂, and the sigmoid's slope is *a*₂ × (1 − *a*₂) (section 43.1); multiplied, they give −(1 − *a*₂) = *a*₂ − *y*:

> dL/d*z*₂ = *a*₂ − *y* = 0.5359 − 1 = **−0.4641**

The same simplification works when *y* = 0, and it's why PyTorch has a loss that combines the sigmoid and log loss into one step (`BCEWithLogitsLoss`, section 43.5).

**Step 2: the output weights.** *z*₂ = 0.5 × *a*₁[0] − 0.6 × *a*₁[1] + 0.2, so nudging the first weight moves *z*₂ by *a*₁[0] per unit: its slope is *a*₁[0]. Chain rule:

> dL/dW2 = (*a*₂ − *y*) × *a*₁ = −0.4641 × [0.2913, 0.3364] = **[−0.1352, −0.1561]**

**Step 3: back into the hidden layer.** The loss reaches hidden neuron *j* through its output weight, then through tanh, whose slope is 1 − tanh(*z*)² (just as the sigmoid's slope has its own formula):

> dL/d*z*₁[*j*] = (*a*₂ − *y*) × W2[*j*] × (1 − *a*₁[*j*]²)
>
> neuron 0: −0.4641 × 0.5 × (1 − 0.2913²) = **−0.2124**
>
> neuron 1: −0.4641 × (−0.6) × (1 − 0.3364²) = **0.2470**

**Step 4: the hidden weights.** Each hidden weight multiplies one input, so its gradient is dL/d*z*₁ for its neuron times that input (1.0 or 0.5):

> dL/dW1 = [[−0.2124 × 1.0, −0.2124 × 0.5], [0.2470 × 1.0, 0.2470 × 0.5]] = **[[−0.2124, −0.1062], [0.2470, 0.1235]]**

Notice the reuse: steps 2 and 3 both start from step 1's −0.4641, and step 4 reuses step 3. On a network with millions of weights, that reuse is what makes backpropagation fast. Now the same four steps in code, next to autograd:

```python
y_true = 1.0
dz2 = a2_hand - y_true  # step 1
dW2 = [dz2 * a1_0, dz2 * a1_1]  # step 2
dz1 = [dz2 * 0.5 * (1 - a1_0**2), dz2 * (-0.6) * (1 - a1_1**2)]  # step 3
dW1 = [[dz1[0] * 1.0, dz1[0] * 0.5], [dz1[1] * 1.0, dz1[1] * 0.5]]  # step 4
print(f"by hand  dL/dW2 = {[round(v, 4) for v in dW2]}")
print(f"by hand  dL/dW1 = {[[round(v, 4) for v in row] for row in dW1]}")
print(f"autograd dL/dW2 = {[round(v, 4) for v in W2g.grad[0].tolist()]}")
```

```
by hand  dL/dW2 = [-0.1352, -0.1561]
by hand  dL/dW1 = [[-0.2124, -0.1062], [0.247, 0.1235]]
autograd dL/dW2 = [-0.1352, -0.1561]
```

- `a2_hand`, `a1_0` and `a1_1` are the by-hand values from section 43.3.
- Each line is one step above, with the weights 0.5 and −0.6 and the inputs 1.0 and 0.5 written in.

The hand calculation and autograd agree on every gradient. That is all `.backward()` does: the chain rule, applied backwards through every layer, automatically.

### Checking with a nudge

Chapter 35 (section 35.4) measured a slope without any calculus: nudge the weight, and see how much the loss moves. Do that for the first output weight. This version nudges both ways, up by `epsilon` and down by `epsilon`, and divides the change by the distance between them, 2 × `epsilon`; it's more accurate than nudging one way.

```python
def nudge_slope(W1, b1, W2, b2, x, target, epsilon=1e-4):
    W2_plus = W2.clone()
    W2_plus[0, 0] += epsilon
    W2_minus = W2.clone()
    W2_minus[0, 0] -= epsilon
    loss_plus = nn.functional.binary_cross_entropy(tiny_forward(W1, b1, W2_plus, b2, x), target)
    loss_minus = nn.functional.binary_cross_entropy(tiny_forward(W1, b1, W2_minus, b2, x), target)
    return ((loss_plus - loss_minus) / (2 * epsilon)).item()


print(f"hand (chain rule):  {dW2[0]:.8f}")
print(f"nudge, 32-bit:      {nudge_slope(W1, b1, W2, b2, x_tiny, target_tiny):.8f}")
```

```
hand (chain rule):  -0.13519938
nudge, 32-bit:      -0.13500452
```

- `W2_plus = W2.clone()` copies the weights, and **`W2_plus[0, 0] += epsilon`** raises the weight in row 0, column 0, the first output weight, by `epsilon` = 0.0001. `W2_minus` lowers it by the same amount.
- `loss_plus` and `loss_minus` are the losses with each nudged weight; the slope is their difference divided by 2 × `epsilon`.

The nudge gives −0.13500 against the hand calculation's −0.13520: close, but only to three decimal places. Is `epsilon` too big? No. The losses here are 32-bit numbers, with about 7 significant digits (section 43.0), and the two losses differ only in their fifth decimal place; dividing that tiny difference by 0.0002 magnifies the rounding in the last digits. (Shrinking `epsilon` would make it *worse*: an even smaller difference, magnified more.) Redo it in 64-bit numbers:

```python
print(f"nudge, 64-bit:      {nudge_slope(W1.double(), b1.double(), W2.double(), b2.double(), x_tiny.double(), target_tiny.double()):.8f}")
```

```
nudge, 64-bit:      -0.13519939
```

- **`.double()`** makes a 64-bit (`torch.float64`) copy of a tensor, the same precision as plain Python numbers and NumPy's `float64`.

**Reading it.** In 64-bit, the nudge agrees with the chain rule to 8 decimal places. So the three methods, by hand, autograd, and nudge-and-measure, give the same gradient; the earlier gap was 32-bit rounding. Neural networks still train in 32-bit, because gradient descent only needs the gradient's direction and rough size, not its eighth digit. **Backpropagation is the chain rule, automated**: exactly the answer a patient, tedious calculation would give, only far faster. You'll never write it by hand again; you now know what `.backward()` does.

---
## 43.5 A network on tabular data

### The same data as Chapter 37

Chapter 37 built churn models with logistic regression, random forests, and gradient boosting on Riverstone's accounts. Here is the same data, the same split, and the same preparation, feeding a small neural network instead. The code reads `../accounts/accounts.csv`; if you haven't built it, run `python ../generate_riverstone_accounts.py` first (Chapter 37, section 37.0).

The first cell is Chapter 37's section 37.0, unchanged: load the accounts, treat the rep numbers as labels, name the feature columns, and split 3,000 / 1,000 / 1,000 with `random_state=37`:

```python
import pandas as pd
from sklearn.model_selection import train_test_split

accounts = pd.read_csv("../accounts/accounts.csv")
accounts["rep_id"] = accounts["rep_id"].astype(str)
CATS = ["segment", "city_tier", "company_size", "rep_id"]
NUMS = [
    "tenure_months",
    "orders_2024",
    "units_2024",
    "revenue_2024",
    "avg_discount_pct",
    "late_payment_days",
    "complaints_2024",
    "categories_bought",
    "days_since_last_order",
    "website_logins_2024",
    "catalog_downloads_2024",
]
rest, test_acc = train_test_split(
    accounts, test_size=0.2, random_state=37, stratify=accounts["churned_2025"]
)
train_acc, valid_acc = train_test_split(
    rest, test_size=0.25, random_state=37, stratify=rest["churned_2025"]
)
print(f"train {len(train_acc):,}   valid {len(valid_acc):,}   test {len(test_acc):,}")
```

```
train 3,000   valid 1,000   test 1,000
```

The second cell is the preparation inside Chapter 37's `clf_pipeline` (section 37.3), used on its own: one-hot encode the categories; fill blanks with the median, add a "was blank" flag, and standardize the numbers. Two lines at the end are new:

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numbers = Pipeline(
    [
        ("fill", SimpleImputer(strategy="median", add_indicator=True)),
        ("scale", StandardScaler()),
    ]
)
prepare = ColumnTransformer(
    [("cat", OneHotEncoder(handle_unknown="ignore"), CATS), ("num", numbers, NUMS)]
)
X_train = prepare.fit_transform(train_acc[CATS + NUMS]).astype("float32")
X_valid = prepare.transform(valid_acc[CATS + NUMS]).astype("float32")
y_train = train_acc["churned_2025"].to_numpy().astype("float32")
y_valid = valid_acc["churned_2025"].to_numpy().astype("float32")
print(f"{X_train.shape[0]:,} training accounts, {X_train.shape[1]} features")
```

```
3,000 training accounts, 25 features
```

- `prepare.fit_transform` learns the medians, means and categories from the training rows only and transforms them; `prepare.transform` applies what it learned to the validation rows (Chapter 36, section 36.9).
- **`.astype("float32")`** is new: PyTorch works in 32-bit numbers (section 43.0), and scikit-learn gives 64-bit ones.
- **`.to_numpy()`** is new too: it turns a pandas Series into a plain NumPy array, which `torch.tensor` can read.
- 25 features: 13 one-hot columns for the four categories, the 11 numbers, and 1 "was blank" flag for `late_payment_days` (Chapter 37).

### From arrays to tensors

```python
Xtr_t = torch.tensor(X_train)
Xva_t = torch.tensor(X_valid)
ytr_t = torch.tensor(y_train)
print("X:", Xtr_t.shape, "  y:", ytr_t.shape)
ytr_t = ytr_t.unsqueeze(1)
print("y after unsqueeze(1):", ytr_t.shape)
```

```
X: torch.Size([3000, 25])   y: torch.Size([3000])
y after unsqueeze(1): torch.Size([3000, 1])
```

- `torch.tensor(...)` turns each NumPy array into a tensor, keeping its `float32` type.
- `y` starts as a flat list of 3,000 numbers, shape `[3000]`. The network will output a *column*, shape `[3000, 1]`: one prediction per row, in a column of width 1. The loss function needs the two shapes to match.
- **`.unsqueeze(1)`** adds a dimension of size 1 in position 1, turning `[3000]` into `[3000, 1]`: the same numbers, stood up as a column. (XOR's targets in section 43.2 were typed as a column from the start.)

### The network

```python
torch.manual_seed(43)
network = nn.Sequential(
    nn.Linear(X_train.shape[1], 16),
    nn.ReLU(),
    nn.Linear(16, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
)
print(network)
for name, param in network.named_parameters():
    print(f"{name:<9} {str(list(param.shape)):<9} {param.numel():>4} numbers")
print(f"total: {sum(p.numel() for p in network.parameters())}")
```

```
Sequential(
  (0): Linear(in_features=25, out_features=16, bias=True)
  (1): ReLU()
  (2): Linear(in_features=16, out_features=8, bias=True)
  (3): ReLU()
  (4): Linear(in_features=8, out_features=1, bias=True)
)
0.weight  [16, 25]   400 numbers
0.bias    [16]        16 numbers
2.weight  [8, 16]    128 numbers
2.bias    [8]          8 numbers
4.weight  [1, 8]       8 numbers
4.bias    [1]          1 numbers
total: 561
```

- 25 inputs go to a hidden layer of 16 ReLU neurons, then to a second hidden layer of 8, then to **one output with no activation after it**. The next cell explains why.
- **`named_parameters()`** lists every parameter tensor with its name: `0.weight` is the weight grid of piece 0 of the `Sequential`, `0.bias` its biases, and so on (the ReLUs, pieces 1 and 3, have no parameters).
- The count: 25 × 16 + 16 = 416, then 16 × 8 + 8 = 136, then 8 × 1 + 1 = 9, for a total of **561**. Logistic regression on the same 25 features has 26 parameters (25 weights and a bias).

### The loss and the optimizer

```python
loss_fn3 = nn.BCEWithLogitsLoss()
optimizer3 = torch.optim.Adam(network.parameters(), lr=0.01)
print(f"loss before training: {loss_fn3(network(Xtr_t), ytr_t).item():.4f}")
```

```
loss before training: 0.6994
```

- The network's last layer outputs a raw weighted sum, which can be any number. A raw score before the sigmoid is called a **logit** (it's the log-odds, *z*, of Chapter 37).
- **`nn.BCEWithLogitsLoss`** takes logits, applies the sigmoid itself, and then computes log loss, in one combined step. That's section 43.4's shortcut (the slope at the output is simply *a* − *y*), and it's more accurate in 32-bit numbers than a separate `nn.Sigmoid()` followed by `nn.BCELoss`. So the network has no sigmoid of its own; to get probabilities, apply `torch.sigmoid` to its output.
- **`torch.optim.Adam`** is gradient descent that adjusts each weight's step size as it goes, bigger where the gradient has been small and steady, smaller where it jumps about (Chapter 35 named it in section 35.6). It usually needs far less learning-rate fiddling than plain SGD; `lr=0.01` is its starting step size.
- Before any training, the loss is about 0.69, close to ln 2: the random network predicts roughly 0.5 for everyone.

### Training

One more word first. An **epoch** is one pass through all the training rows. Here every step uses all 3,000 rows at once (called **full-batch** training), so one epoch is one step. Real networks usually take many steps per epoch on small random batches of rows, Chapter 35's stochastic gradient descent; Chapter 53 does that.

```python
from sklearn.metrics import roc_auc_score

for epoch in range(200):
    optimizer3.zero_grad()
    logits = network(Xtr_t)
    loss3 = loss_fn3(logits, ytr_t)
    loss3.backward()
    optimizer3.step()
    if epoch % 40 == 0:
        with torch.no_grad():
            valid_pred = torch.sigmoid(network(Xva_t)).numpy().ravel()
        print(
            f"epoch {epoch:>3}: training loss {loss3.item():.4f}   "
            f"validation AUC {roc_auc_score(y_valid, valid_pred):.3f}"
        )

with torch.no_grad():
    final_pred = torch.sigmoid(network(Xva_t)).numpy().ravel()
print(f"after 200 epochs: validation AUC {roc_auc_score(y_valid, final_pred):.3f}")
```

```
epoch   0: training loss 0.6994   validation AUC 0.542
epoch  40: training loss 0.2510   validation AUC 0.745
epoch  80: training loss 0.2404   validation AUC 0.763
epoch 120: training loss 0.2341   validation AUC 0.766
epoch 160: training loss 0.2262   validation AUC 0.771
after 200 epochs: validation AUC 0.773
```

- The first five lines inside the loop are section 43.2's training step.
- `if epoch % 40 == 0:` reports every 40th epoch (`%` is the remainder: 0, 40, 80, …), so the output stays short. The training loss printed is the one computed *before* that epoch's step.
- **`with torch.no_grad():`** means "don't keep a gradient record for what happens inside": we're only scoring the validation rows, not training on them, so there's nothing to backpropagate. Without the record, PyTorch can also hand the result straight to NumPy with `.numpy()`.
- `torch.sigmoid(network(Xva_t))` turns the validation logits into churn probabilities, and `roc_auc_score` is Chapter 36's AUC.

**Reading it.** Training loss falls steadily and validation AUC climbs from a coin toss (0.542) to 0.773: Chapter 35's gradient descent, now adjusting 561 parameters across three layers instead of one.

### The honest comparison

Now logistic regression and Chapter 37's tuned gradient boosting (`hgb_settings`, section 37.8), fitted on the same 3,000 rows and scored on the same 1,000 validation accounts:

```python
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

logit_model = LogisticRegression(max_iter=2000).fit(X_train, y_train)
logit_pred = logit_model.predict_proba(X_valid)[:, 1]

boosting_model = HistGradientBoostingClassifier(
    learning_rate=0.05, max_depth=3, min_samples_leaf=40, max_iter=300, random_state=37
).fit(X_train, y_train)
boosting_pred = boosting_model.predict_proba(X_valid)[:, 1]

print(f"{'model':<24} AUC     log loss   parameters")
for name, pred, size in [
    ("logistic regression", logit_pred, "26"),
    ("small neural network", final_pred, "561"),
    ("gradient boosting", boosting_pred, "(300 trees)"),
]:
    print(f"{name:<24} {roc_auc_score(y_valid, pred):.3f}   {log_loss(y_valid, pred):.4f}     {size}")
```

```
model                    AUC     log loss   parameters
logistic regression      0.764   0.2833     26
small neural network     0.773   0.2812     561
gradient boosting        0.786   0.2744     (300 trees)
```

- Both models are Chapter 37's, with its settings; boosting's are the four in `hgb_settings`. They take the same prepared arrays as the network. (Boosting doesn't need the scaling, but it doesn't mind it: trees only compare values within one column.)
- The loop goes through three (name, predictions, size) triples and prints one row each.

**Reading it, plainly.** The small network (0.773) and logistic regression (0.764) are **effectively tied**: Chapter 37 (section 37.8) showed that with 1,000 validation accounts and 97 churners, differences of about 0.01 are noise. Tuned gradient boosting (0.786) is ahead of both, and Chapter 37's cross-validation (section 37.10) showed that boosting's lead over logistic regression on this data is real. So the network matches the simple model at twenty times the parameters, with more code, more settings, and more training time, and trails boosting. **On clean, modest-sized tabular data, deep learning has no automatic advantage** over the methods of earlier chapters; tuned gradient boosting remains the strongest default for tables of numbers.

### The test set, once

The network's size, its 200 epochs, and the comparison above were all judged on the validation set, so those numbers flatter whichever choices we made by looking at them (Chapter 39, section 39.7). The honest final number comes from the test set, scored once:

```python
X_test = prepare.transform(test_acc[CATS + NUMS]).astype("float32")
y_test = test_acc["churned_2025"].to_numpy()
with torch.no_grad():
    network_test = torch.sigmoid(network(torch.tensor(X_test))).numpy().ravel()
for name, pred in [
    ("logistic regression", logit_model.predict_proba(X_test)[:, 1]),
    ("small neural network", network_test),
    ("gradient boosting", boosting_model.predict_proba(X_test)[:, 1]),
]:
    print(f"{name:<24} test AUC {roc_auc_score(y_test, pred):.3f}   log loss {log_loss(y_test, pred):.4f}")
```

```
logistic regression      test AUC 0.797   log loss 0.2547
small neural network     test AUC 0.818   log loss 0.2498
gradient boosting        test AUC 0.821   log loss 0.2437
```

- `prepare.transform` prepares the 1,000 test accounts with what it learned from the training rows, exactly as for validation.
- Each model is scored once; nothing is changed after seeing these numbers.

**Reading it.** On the test set the network (0.818) lands between logistic regression (0.797) and boosting (0.821), and much closer to boosting than on validation. That's the noise Chapter 37 warned about: on 1,000 accounts, a gap of 0.003 is a tie, and even 0.02 is only suggestive. Put the two scorings together and the honest summary is that the network is in the same range as the other two and **never clearly ahead of boosting**, for far more code, settings and training time. These are single scores on 1,000 accounts, trained on 3,000 rows, so they aren't the same as Chapter 37's section 37.11 test scores, which used models refitted on all 4,000 non-test accounts. on 1,000 accounts, trained on 3,000 rows, so they aren't the same as Chapter 37's section 37.11 test scores, which used models refitted on all 4,000 non-test accounts; the order is what matters. Where deep learning's advantage becomes overwhelming is where the simpler methods have no good equivalent at all: raw images, audio, and text at scale. That's where the next two sections go.

---

## 43.6 A first image classifier

### An image is a grid of numbers

scikit-learn includes 1,797 small handwritten digits, scanned as 8 × 8 grids of brightness values from 0 to 16. `load_digits` loads them from the library itself, with no download:

```python
from sklearn.datasets import load_digits

digits = load_digits()
images = digits.images.astype("float32") / 16.0  # 0-16 -> 0-1
labels = digits.target
print(f"{len(images):,} images, each {images.shape[1]}x{images.shape[2]} pixels")
print("digits:", np.unique(labels))
print("the first image, rounded to 1 decimal:")
print(np.round(images[0], 1))
print(f"label: {labels[0]}")
```

```
1,797 images, each 8x8 pixels
digits: [0 1 2 3 4 5 6 7 8 9]
the first image, rounded to 1 decimal:
[[0.  0.  0.3 0.8 0.6 0.1 0.  0. ]
 [0.  0.  0.8 0.9 0.6 0.9 0.3 0. ]
 [0.  0.2 0.9 0.1 0.  0.7 0.5 0. ]
 [0.  0.2 0.8 0.  0.  0.5 0.5 0. ]
 [0.  0.3 0.5 0.  0.  0.6 0.5 0. ]
 [0.  0.2 0.7 0.  0.1 0.8 0.4 0. ]
 [0.  0.1 0.9 0.3 0.6 0.8 0.  0. ]
 [0.  0.  0.4 0.8 0.6 0.  0.  0. ]]
label: 0
```

- `digits.images` is a NumPy array of shape (1,797, 8, 8): 1,797 grids of 8 rows and 8 columns. Dividing by 16 rescales every value to between 0 and 1, and `.astype("float32")` gets it ready for PyTorch.
- `digits.target` holds the true digit of each image, and `np.unique(labels)` lists the distinct values: 0 to 9.
- In this data **a high value means ink**: 0 is blank paper, 1 is solid ink. Look at the grid and you can see the "0": a ring of higher values with low values in the middle.

### A convolution, one position at a time

A **convolution** slides a small grid of weights, a **kernel** (or **filter**), across the image. At each position it multiplies the kernel by the patch of image under it, cell by cell, and adds the results: a weighted sum, like a neuron's. Here's one kernel, designed by hand, applied at one position (rows 2–4, columns 2–4):

```python
edge_kernel = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
patch = images[0][2:5, 2:5]
print(np.round(patch, 2))
print(f"weighted sum at this position: {(patch * edge_kernel).sum():.2f}")
```

```
[[0.94 0.12 0.  ]
 [0.75 0.   0.  ]
 [0.5  0.   0.  ]]
weighted sum at this position: -0.56
```

- `edge_kernel` has −1s on its top row and +1s on its bottom row, so it computes (ink in the bottom row) − (ink in the top row): positive where ink *increases* going down, negative where it *decreases*. It detects **horizontal edges**.
- `images[0][2:5, 2:5]` slices rows 2 to 4 and columns 2 to 4 (Chapter 18's NumPy slicing: the end is excluded).
- `patch * edge_kernel` multiplies cell by cell; `.sum()` adds the nine products.

This patch sits on the *left side* of the "0", a vertical stroke, where ink decreases only slightly going down, so the answer is a small −0.56. One position says little. Slide the kernel over every position:

```python
feature_map = np.zeros((6, 6))
for row in range(6):
    for col in range(6):
        feature_map[row, col] = (images[0][row : row + 3, col : col + 3] * edge_kernel).sum()
print(np.round(feature_map, 1))
```

```
[[ 0.8  0.1 -0.6 -0.6  0.6  1.1]
 [ 0.2 -0.8 -1.6 -2.  -0.9 -0.2]
 [-0.3 -0.4 -0.6 -0.2 -0.1 -0.1]
 [-0.1 -0.1  0.   0.3  0.2  0.2]
 [ 0.2  0.5  1.3  1.1  0.3 -0.3]
 [-0.6  0.2  1.1  0.6 -0.6 -1.2]]
```

- An 8 × 8 image has 6 × 6 positions where a 3 × 3 kernel fits entirely inside it, so `np.zeros((6, 6))` makes a 6 × 6 grid of zeros to fill in.
- The two loops visit every position; `images[0][row : row + 3, col : col + 3]` is the 3 × 3 patch whose top-left corner is at (`row`, `col`).

**Reading it.** The grid a convolution produces is called a **feature map**: it shows where in the image the kernel's pattern appears. The largest positive values are along the **bottom** of the "0", where ink increases going down into the lower stroke; the most negative, −2.0, are just **under the top stroke**, where ink ends going down; near the flat middle and edges, the values are close to 0. Figure 43.3 shows the image, the kernel, and the feature map side by side. (Strictly, this sliding weighted sum is called *cross-correlation*; PyTorch's convolution layers compute exactly this, and everyone calls it convolution.)

![Three grids side by side: the 8 by 8 image of the digit 0 shaded by ink; the 3 by 3 kernel with -1 in the top row, 0 in the middle row and +1 in the bottom row; and the 6 by 6 feature map, with the largest positive values along the bottom of the 0, marked with plus signs, and the most negative just under the top stroke, marked with minus signs](figures/fig43-3-convolution.svg)

*Figure 43.3 — A horizontal-edge kernel slid across the first digit. Positive values (+) mark where ink begins going down; negative values (−) mark where it ends.*

A **convolutional neural network** (CNN) has layers of such kernels, but nobody designs them: they start random and are learned by gradient descent, each ending up detecting whatever pattern helps reduce the loss. Early layers tend to learn edges and strokes; later layers combine them into loops and shapes.

A CNN also uses **pooling**, which shrinks a feature map by keeping one number per small region. **Max pooling** over 2 × 2 regions keeps the largest value in each, so a 4 × 4 map becomes 2 × 2: each region of four numbers, such as [0.1, 0.9, 0.3, 0.2], becomes its maximum, 0.9. The network keeps "the pattern appeared somewhere around here" and drops the exact position, with four times fewer numbers.

### A CNN as a class

So far every network was an `nn.Sequential`, a straight chain. This one is written as a **class** (Chapter 29, section 29.5), because section 43.7 needs to reach inside it and use its two halves separately: the *feature* part (the convolutions) and the *classifier* part (the final layers).

```python
class SmallCNN(nn.Module):
    def __init__(self, n_classes):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 8, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(16 * 2 * 2, 32)
        self.fc2 = nn.Linear(32, n_classes)

    def features(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        return torch.relu(self.fc1(x.flatten(1)))

    def forward(self, x):
        return self.fc2(self.features(x))


torch.manual_seed(43)
base_model = SmallCNN(n_classes=5)
print(f"parameters: {sum(p.numel() for p in base_model.parameters()):,}")
```

```
parameters: 3,493
```

- **`class SmallCNN(nn.Module):`** makes `SmallCNN` a kind of `nn.Module`, PyTorch's class for anything that is a network or part of one. It's the inheritance of Chapter 29 (`class NoDataError(ReportError)`), with a class from a library as the parent.
- **`super().__init__()`** runs the parent class's own `__init__` first. PyTorch's `nn.Module` needs its setup to run before you store any layers; leave this line out and the next line fails. Every PyTorch model class starts its `__init__` this way.
- Layers stored on `self` (`self.conv1`, …) are found automatically by `.parameters()`, so an optimizer sees them all.
- **`nn.Conv2d(1, 8, kernel_size=3, padding=1)`** is a convolutional layer: it takes **1** input grid (a grey image has one brightness value per pixel; a colour image would have 3), learns **8** different 3 × 3 kernels (`kernel_size=3`), and outputs 8 feature maps. **`padding=1`** adds a border of zeros around the grid first, so a 3 × 3 kernel fits at every one of the 8 × 8 positions and the output stays 8 × 8 instead of shrinking to 6 × 6.
- `nn.Conv2d(8, 16, ...)` takes those 8 maps and learns 16 kernels, each looking at all 8 maps at once.
- **`nn.MaxPool2d(2)`** is 2 × 2 max pooling: it halves the width and height.
- **`features`** is a method (Chapter 29) that runs convolution, ReLU, pooling, twice, then flattens and applies `fc1`. **`x.flatten(1)`** keeps dimension 0 (one entry per image) and flattens everything after it into one row per image: 16 maps of 2 × 2 become 64 numbers, which is where `16 * 2 * 2` in `fc1` comes from.
- **`forward`** is what runs when you call the model, `model(x)`: here the features, then the final layer `fc2`, which outputs one score per class.
- `SmallCNN(n_classes=5)` builds one for five classes (the next cell uses digits 0–4). `torch.manual_seed(43)` fixes its random starting kernels.

Where do 3,493 parameters come from? Each kernel has 9 weights per input map, plus one bias per kernel:

| Layer | Calculation | Parameters |
|---|---|---:|
| `conv1` | 1 input map × 8 kernels × 9 weights + 8 biases | 80 |
| `conv2` | 8 input maps × 16 kernels × 9 weights + 16 biases | 1,168 |
| `fc1` | 64 inputs × 32 neurons + 32 biases | 2,080 |
| `fc2` | 32 inputs × 5 outputs + 5 biases | 165 |
| **Total** | | **3,493** |

### The data, and the shapes

The CNN will learn the digits 0 to 4; section 43.7 keeps 5 to 9 aside for transfer learning.

```python
base_mask = labels < 5
X_base, y_base = images[base_mask], labels[base_mask]
Xb_train, Xb_test, yb_train, yb_test = train_test_split(
    X_base, y_base, test_size=0.25, random_state=43, stratify=y_base
)


def to_tensors(images_, labels_):
    return torch.tensor(images_).unsqueeze(1), torch.tensor(labels_).long()


Xb_train_t, yb_train_t = to_tensors(Xb_train, yb_train)
Xb_test_t, yb_test_t = to_tensors(Xb_test, yb_test)
print(f"digits 0-4: {len(Xb_train):,} training images, {len(Xb_test):,} test images")
print("image tensor shape:", Xb_train_t.shape)
```

```
digits 0-4: 675 training images, 226 test images
image tensor shape: torch.Size([675, 1, 8, 8])
```

- `labels < 5` is a mask, True for the digits 0 to 4 (Chapter 18's boolean filtering); `images[base_mask]` keeps those images.
- `train_test_split` holds out 25%, stratified so each digit keeps its share (Chapter 36).
- `to_tensors` does two conversions. **`.unsqueeze(1)`** adds the "input maps" dimension that `Conv2d` expects: shape (images, maps, rows, columns), with 1 map. **`.long()`** stores the labels as whole numbers (64-bit integers); the multi-class loss below needs class numbers, not decimals. The name `images_`, with a trailing underscore, just avoids reusing the name `images`.

Follow one image through the network and watch its shape at every step:

```python
x = Xb_train_t[:1]
print("input     ", list(x.shape))
x = base_model.pool(torch.relu(base_model.conv1(x)))
print("conv1+pool", list(x.shape))
x = base_model.pool(torch.relu(base_model.conv2(x)))
print("conv2+pool", list(x.shape))
x = x.flatten(1)
print("flatten   ", list(x.shape))
x = torch.relu(base_model.fc1(x))
print("fc1       ", list(x.shape))
print("fc2       ", list(base_model.fc2(x).shape))
```

```
input      [1, 1, 8, 8]
conv1+pool [1, 8, 4, 4]
conv2+pool [1, 16, 2, 2]
flatten    [1, 64]
fc1        [1, 32]
fc2        [1, 5]
```

- `Xb_train_t[:1]` is the first image, kept as a batch of one: shape [1, 1, 8, 8].
- `conv1` makes 8 maps of 8 × 8 (the padding keeps the size), and pooling halves them to 4 × 4. `conv2` makes 16 maps of 4 × 4, pooled to 2 × 2. Flattening gives 16 × 2 × 2 = 64 numbers; `fc1` turns them into 32 and `fc2` into 5 scores, one per digit.

### From two classes to five

Until now every model had one output: a single logit, turned into one probability by the sigmoid. With five digits the last layer outputs **five** logits, one per class. You met the function that turns several scores into probabilities in Chapter 41 (section 41.4): **softmax**, the many-class version of the sigmoid. It makes every score positive and scales them so they add up to 1. The predicted class is the one with the highest score. Here it is on the untrained network's five scores for one image:

```python
scores = base_model(Xb_train_t[:1])
print("logits:     ", [round(v, 3) for v in scores[0].tolist()])
print("softmax:    ", [round(v, 3) for v in torch.softmax(scores, dim=1)[0].tolist()])
print("argmax:     ", scores.argmax(1).item(), "   true label:", yb_train_t[0].item())
```

```
logits:      [-0.101, 0.091, 0.114, -0.107, -0.138]
softmax:     [0.185, 0.224, 0.229, 0.184, 0.178]
argmax:      2    true label: 4
```

- `scores[0]` is the only row of the 1 × 5 output.
- **`torch.softmax(scores, dim=1)`** applies softmax across dimension 1, the five scores of each row; the five probabilities add up to 1.
- **`.argmax(1)`** gives the *position* of the largest value along dimension 1: the predicted class.
- Untrained, the five probabilities are all near 0.2, a guess.

The multi-class loss is **`nn.CrossEntropyLoss`**. It takes the raw logits, applies softmax itself (as `BCEWithLogitsLoss` applies the sigmoid), and takes −ln of the probability given to the true class, averaged over the images: Chapter 35's log loss, for more than two classes. That's why the network's `forward` ends with `fc2` and no activation.

### Training the CNN

```python
optimizer4 = torch.optim.Adam(base_model.parameters(), lr=0.01)
loss_fn4 = nn.CrossEntropyLoss()

for epoch in range(60):
    optimizer4.zero_grad()
    loss4 = loss_fn4(base_model(Xb_train_t), yb_train_t)
    loss4.backward()
    optimizer4.step()

with torch.no_grad():
    predicted = base_model(Xb_test_t).argmax(1)
base_accuracy = (predicted == yb_test_t).float().mean().item()
print(f"after 60 epochs: training loss {loss4.item():.4f}   test accuracy {base_accuracy:.1%}")
```

```
after 60 epochs: training loss 0.0019   test accuracy 98.7%
```

- The loop is the same five-line training step, now with `CrossEntropyLoss` and the labels as class numbers.
- `base_model(Xb_test_t).argmax(1)` predicts a digit for every test image.
- `predicted == yb_test_t` gives True or False per image; **`.float()`** turns those into 1.0 and 0.0, and `.mean()` of them is the share correct, the **accuracy**.

**Reading it.** With 675 training images and a network of only 3,493 parameters, tiny by deep-learning standards, the model classifies 98.7% of the 226 held-out images of the digits 0–4 correctly. Two rounds of convolution and pooling turn each 8 × 8 grid into a compact set of features that a small final layer can classify.

> **Learned features are learned representations.** For each image, `base_model.features(...)` produces 32 numbers: the network's own description of that image, learned by gradient descent. It's the image version of Chapter 41's word embeddings (section 41.7), where each word became a vector learned from text. Nobody told the network what the 32 numbers should mean, yet images of the same digit end up with more similar vectors than images of different digits. Section 43.7 works by reusing exactly these 32-number descriptions on a new task.

---
## 43.7 Transfer learning

### The idea

Training a network from nothing needs a reasonable amount of data. **Transfer learning** starts instead from a network already trained on a *related* task, the **base task**, and reuses what it learned. The usual recipe: keep its early layers, which have learned general-purpose features, **freeze** them (so training doesn't change them), and train only new final layers on the new, smaller task. The reasoning: kernels that learned to detect edges and strokes for one set of digits should find similar edges and strokes in other digits, without relearning them.

The new task here is the digits 5 to 9, relabelled 0 to 4 so the same five-output head fits, with only a handful of training examples per digit:

```python
new_mask = labels >= 5
X_new, y_new = images[new_mask], labels[new_mask] - 5  # 5-9 become 0-4
Xn_train, Xn_test, yn_train, yn_test = train_test_split(
    X_new, y_new, test_size=0.25, random_state=43, stratify=y_new
)
Xn_test_t, yn_test_t = to_tensors(Xn_test, yn_test)


def small_training_set(n_per_class, seed):
    rng = np.random.default_rng(seed)
    chosen = []
    for digit_class in range(5):
        candidates = np.where(yn_train == digit_class)[0]
        chosen.extend(rng.choice(candidates, n_per_class, replace=False))
    return to_tensors(Xn_train[chosen], yn_train[chosen])


Xs, ys = small_training_set(10, seed=0)
print(f"new task: {len(Xn_train)} training images available, {len(Xn_test)} test images")
print(f"one small training set: {len(Xs)} images, labels {ys.tolist()}")
```

```
new task: 672 training images available, 224 test images
one small training set: 50 images, labels [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
```

- `labels[new_mask] - 5` relabels 5, 6, 7, 8, 9 as 0 to 4.
- `small_training_set(n_per_class, seed)` picks `n_per_class` random training images of each digit. **`np.random.default_rng(seed)`** makes NumPy's random generator with a fixed seed, so the same seed always picks the same images. `np.where(yn_train == digit_class)[0]` lists the positions of that digit's images, and `rng.choice(candidates, n_per_class, replace=False)` picks `n_per_class` of them, none twice.
- The test set, 224 images, is the same for every experiment below.

### One transfer run, step by step

Start from a copy of the trained digit model:

```python
import copy

torch.manual_seed(0)
transfer_model = copy.deepcopy(base_model)
for param in transfer_model.conv1.parameters():
    param.requires_grad = False
for param in transfer_model.conv2.parameters():
    param.requires_grad = False
transfer_model.fc1 = nn.Linear(16 * 2 * 2, 32)
transfer_model.fc2 = nn.Linear(32, 5)
trainable = [p for p in transfer_model.parameters() if p.requires_grad]
print(f"trainable parameters: {sum(p.numel() for p in trainable):,} of {sum(p.numel() for p in transfer_model.parameters()):,}")
```

```
trainable parameters: 2,245 of 3,493
```

- **`copy.deepcopy(base_model)`** makes a complete, independent copy, weights and all. Changing the copy can't damage `base_model`, which the later runs need unchanged.
- **`param.requires_grad = False`** freezes a parameter: `backward()` no longer computes its gradient, so the optimizer never changes it. The two loops freeze both convolutional layers, the 80 + 1,168 = 1,248 parameters that detect strokes.
- Assigning new `nn.Linear` layers to `fc1` and `fc2` replaces the old classifier with a fresh, random one: the **head**. `torch.manual_seed(0)` fixes its starting weights.
- `trainable` is a list comprehension (Chapter 17) that keeps only the parameters still being trained: 2,080 + 165 = 2,245 of the 3,493.

Now train only the head, for 80 epochs, on the 50 images, and score it on the 224 test images:

```python
optimizer5 = torch.optim.Adam(trainable, lr=0.01)
for epoch in range(80):
    optimizer5.zero_grad()
    loss5 = loss_fn4(transfer_model(Xs), ys)
    loss5.backward()
    optimizer5.step()
with torch.no_grad():
    accuracy = (transfer_model(Xn_test_t).argmax(1) == yn_test_t).float().mean().item()
print(f"transfer, 10 per class: test accuracy {accuracy:.1%}")
```

```
transfer, 10 per class: test accuracy 92.0%
```

- `torch.optim.Adam(trainable, ...)` hands the optimizer only the trainable parameters.
- The rest is section 43.6's training and scoring.

### Transfer against training from scratch

Is 92.0% good? Only a comparison can say. Wrap the steps above into a function, and write a second one that trains a fresh `SmallCNN` from scratch on the **same** images. Each takes the training images and a seed, so both methods see identical data:

```python
def train_transfer(Xs, ys, seed, epochs=80):
    torch.manual_seed(seed)
    model = copy.deepcopy(base_model)
    for param in model.conv1.parameters():
        param.requires_grad = False
    for param in model.conv2.parameters():
        param.requires_grad = False
    model.fc1 = nn.Linear(16 * 2 * 2, 32)
    model.fc2 = nn.Linear(32, 5)
    trainable = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.Adam(trainable, lr=0.01)
    for epoch in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn4(model(Xs), ys)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        return (model(Xn_test_t).argmax(1) == yn_test_t).float().mean().item()


def train_scratch(Xs, ys, seed, epochs=80):
    torch.manual_seed(seed)
    model = SmallCNN(n_classes=5)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    for epoch in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn4(model(Xs), ys)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        return (model(Xn_test_t).argmax(1) == yn_test_t).float().mean().item()


print(f"transfer, seed 0: {train_transfer(Xs, ys, seed=0):.1%}")
print(f"scratch,  seed 0: {train_scratch(Xs, ys, seed=0):.1%}")
```

```
transfer, seed 0: 92.0%
scratch,  seed 0: 94.6%
```

- `train_transfer` is the two cells above, as a function; with seed 0 it repeats the run exactly.
- `train_scratch` is the same minus the copying and freezing: every one of the 3,493 parameters starts random and is trained.
- `torch.manual_seed(seed)` at the start of each makes every run repeatable.

One run of each is one draw: a different 50 images, or different starting weights, would give different numbers. So repeat each training-set size with five seeds (five different samples of images, and five different starting weights), give both methods the same sample each time, and report the average and the range:

```python
print(f"{'examples/class':>14}   {'transfer: mean (range)':>24}   {'scratch: mean (range)':>23}")
sweep = {}
for n in [3, 5, 10, 15, 30]:
    transfer_runs, scratch_runs = [], []
    for seed in range(5):
        Xs, ys = small_training_set(n, seed)
        transfer_runs.append(train_transfer(Xs, ys, seed))
        scratch_runs.append(train_scratch(Xs, ys, seed))
    sweep[n] = (transfer_runs, scratch_runs)
    t, s = np.array(transfer_runs), np.array(scratch_runs)
    print(
        f"{n:>14}   {t.mean():>9.1%} ({t.min():.0%}-{t.max():.0%})   "
        f"{s.mean():>8.1%} ({s.min():.0%}-{s.max():.0%})"
    )
```

```
examples/class     transfer: mean (range)     scratch: mean (range)
             3       80.5% (75%-84%)      83.9% (78%-92%)
             5       86.5% (83%-88%)      89.0% (88%-91%)
            10       90.4% (83%-93%)      93.4% (88%-95%)
            15       92.2% (91%-94%)      94.5% (94%-96%)
            30       94.2% (93%-95%)      96.2% (95%-97%)
```

- For each size `n`, the inner loop draws five samples (`seed` 0 to 4) and trains both methods on each; `sweep[n]` keeps the ten scores for later.
- `np.array(...)` turns each list of five scores into an array, so `.mean()`, `.min()` and `.max()` work.

**Reading it, honestly.** Training from scratch comes out ahead **at every size**, by 2 to 3 points on average, and transfer learning from this base never wins on average. The ranges overlap at the small sizes (at 3 per class, transfer runs from 75% to 84% and scratch from 78% to 92%), so single runs can point either way: one draw of each could easily have made transfer look better at some size. That's why each cell is five runs on shared samples. Both methods improve steadily with more examples, from about 81–84% at 3 per class to 94–96% at 30.

**Why doesn't transfer learning dominate here, the way its reputation suggests?** Because the *base* task, recognizing digits 0–4 from only 675 small images, is itself small and narrow. Transfer learning's dramatic real-world wins come from base models trained on **enormous, general** datasets: a network trained on millions of varied photographs learns edge and texture detectors far richer than anything 675 tiny digit images can teach, and *that* richness is what transfers to a new, small task. **The lesson isn't "transfer learning doesn't work"; it's "transfer learning is only as good as what the base model actually learned,"** and that has to be checked, not assumed, like every other technique in this book.

One middle way deserves a name. **Fine-tuning** unfreezes some of the pretrained layers, usually the later ones, and trains them a little along with the new head, so the reused features can adapt to the new task. Exercise 11 tries it.

> **Watch out: "pretrained" is doing a lot of work in that sentence.** In practice, most transfer learning starts from a model trained on a dataset far larger and more general than anything in this chapter (millions of natural images, or, for text, billions of words: Chapter 54). The small, honest example here demonstrates the *mechanism*; don't extrapolate its numbers to production transfer learning, where the base model's training data is usually the deciding factor.

---

## 43.8 When to reach for deep learning

| Situation | Reach for |
|---|---|
| Tabular data (a table of customer, transaction, or account features) | Gradient boosting or logistic regression first (Chapter 37); a network rarely beats a well-tuned boosted model here |
| Images | A convolutional network, ideally starting from a strong pretrained base (transfer learning), not from scratch |
| Text at scale | Modern pretrained language models (Chapter 54) rather than a network trained from nothing |
| A small dataset (hundreds to low thousands of rows) | Simpler methods generally need less data to generalize well; deep learning shines with much more data |
| You need to explain individual predictions to a regulator or manager | Simpler models (Chapters 37, 39) are far easier to interpret than a deep network |
| Millions of rows, complex interactions, and no interpretability requirement | Deep learning becomes competitive with, and sometimes ahead of, boosted trees |

The pattern across this book has been consistent: try the simplest thing that could work, measure it honestly, and only add complexity that earns its place with evidence (Chapter 36's baselines, Chapter 37's algorithm comparisons). Deep learning is not an exception to that discipline; it's one more tool to test against it.

---
## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Reaching for a neural network on tabular data by default | More code, more tuning, no better result than boosting | Compare against Chapter 37's methods before committing |
| No hidden layer, or no activation function between layers | The network behaves like plain linear or logistic regression | Add at least one hidden layer with a nonlinear activation (ReLU, tanh) |
| Sigmoid in every hidden layer of a deep network | Training stalls; gradients shrink toward zero | Use ReLU (or a variant) in hidden layers; keep sigmoid for the output |
| Forgetting `optimizer.zero_grad()` | Gradients add up across steps; the loss behaves erratically | Zero the gradients at the start of every training step |
| A `nn.Sigmoid()` layer followed by `BCEWithLogitsLoss` (a double sigmoid) | The loss sees every probability squeezed between 0.5 and 0.73, so training goes badly | Remove the final `Sigmoid`; the loss applies it |
| Raw logits fed into `BCELoss` | An error: `all elements of input should be between 0 and 1` | Use `BCEWithLogitsLoss`, or add a final `nn.Sigmoid()` |
| Assuming transfer learning always helps | No improvement, or a worse result, than training from scratch | Check what the base model was trained on and how much data you have |
| Judging a deep learning result without a baseline | "95% accuracy!" with no comparison | Always compare with Chapter 37's algorithms (and a base-rate check from Chapter 35) |
| Training and evaluating on the same data | Impressive numbers that don't hold up | Chapter 36's splits and Chapter 39's evaluation habits apply unchanged |

---

## In the real world: "Should our churn model be a neural network?"

In October 2026, Vikram comes back from a retail-technology conference where a speaker presented a "deep learning churn model" with 91% accuracy. His question for Meera: should Riverstone's churn model be upgraded to deep learning?

Meera doesn't need a new project to answer. This chapter's comparison already ran on Riverstone's own accounts, scored once on the test set: the small neural network reached a test AUC of 0.818, logistic regression 0.797, and tuned gradient boosting 0.821. And the conference number needs one more fact before it means anything: Riverstone's churn rate is 9.7%, so predicting "no churn" for everyone is already 90.3% accurate. A 91% headline says almost nothing on a problem this imbalanced, as Chapter 39 established.

Her note to Vikram is short: *"On our own accounts, a neural network scores in the same range as the models we already have, and no better than the boosting model; it would cost more to build, retrain, and explain to the sales team. So no upgrade for churn. The 91% from the talk isn't evidence either way: on our 9.7% churn rate, saying 'no churn' for everyone scores 90.3%. If we ever take on an image or text problem, such as sorting photos of damaged products, that's where deep learning would be the right tool to test first."*

The point isn't that deep learning is overhyped; this chapter's own numbers show it does real, useful things, on the right problems. The point is that "deep learning" is a *method*, not a *result*, and every method in this book, however sophisticated, still has to clear the same bar: beat the baseline, on your own data, measured honestly.

---

## Project: a tabular network and an image classifier, evaluated honestly

**Goal:** hands-on practice building, training, and, most importantly, fairly evaluating two small neural networks, one on tabular data and one on images.

### Tools you'll need

- **PyTorch** 2.14.0 (installed in section 43.0; the CPU-only build is all this chapter needs): tensors, `nn.Linear`, `nn.Conv2d`, `nn.MaxPool2d`, `nn.ReLU`, `nn.Tanh`, `nn.Sigmoid`, `nn.Sequential`, `nn.Module`, `nn.BCELoss`, `nn.BCEWithLogitsLoss`, `nn.CrossEntropyLoss`, `torch.optim.SGD`, `torch.optim.Adam`, and `.backward()` for automatic gradients.
- **scikit-learn** 1.9.1 (installed in Chapter 35): `load_digits` (a small image dataset built into the library, no download needed), plus the same splitting, preparation, models and metrics used throughout Part 4.
- Not used here but worth knowing: **torchvision** (pretrained image models; downloading their weights needs an internet connection), **Keras/TensorFlow** (an alternative to PyTorch with a similar feature set), and **TensorBoard** or **Weights & Biases** (tracking training runs, essential once experiments multiply).
- The outputs in this chapter were produced on one CPU core with Python 3.11, PyTorch 2.14.0, scikit-learn 1.9.1, NumPy 2.4.6 and pandas 3.0.6, on 29 September 2026. The whole chapter, exercises included, runs in under a minute. On a computer that lets PyTorch use several CPU cores, the last digit of a few long training runs can come out slightly different, because the cores add numbers up in a different order.
- **Companion files:** this chapter needs no new dataset. `companion/accounts/accounts.csv` is built by `companion/generate_riverstone_accounts.py` (Chapter 37), and the digits come with scikit-learn. Run the chapter's code from `companion/ch43/`.

**Steps:**

1. **Neuron and XOR.** Reproduce section 43.2's single-neuron failure and two-layer success on XOR. Then design a slightly harder toy problem, by hand, that also can't be solved by a straight line, and confirm a hidden layer solves it.
2. **Forward pass by hand.** Pick your own tiny set of weights (2 inputs, 2 or 3 hidden neurons, 1 output) and compute the forward pass on paper before checking it in PyTorch.
3. **Backward pass by hand.** For the same network, compute the gradient of at least one output weight and one hidden weight with the chain rule, as section 43.4 did, and check both against autograd and a 64-bit nudge.
4. **Tabular network.** Train a small network on the Riverstone accounts data (or your own tabular dataset), and compare it honestly with logistic regression and gradient boosting using Chapter 39's metrics (AUC, log loss), not just accuracy. Score the test set once, at the end.
5. **Image classifier.** Train a small CNN on the digits dataset (or another small image dataset), and report a proper held-out accuracy.
6. **Transfer learning.** Split your image classes into a "base" and a "new" task as section 43.7 did, and test transfer learning against training from scratch at several training-set sizes, on the same samples, over several seeds. Report the honest result, whichever way it goes.
7. **Write a one-page recommendation:** for your tabular problem, which method would you actually deploy, and why? For your image problem, at what point (if any) does transfer learning pay off?

**Stretch goals:**

- Add **dropout** (`nn.Dropout`, which switches off a random share of neurons at each training step so the network can't rely on any one of them; Chapter 53 explains it) to the tabular network and see whether it changes the validation AUC.
- Try a **deeper** network (more hidden layers) on the tabular data and check whether validation performance improves or gets worse; connect the result to Chapter 37's bias–variance discussion (section 37.10).
- Use `torchvision.datasets` (if your internet access allows the download) to try transfer learning from a model actually pretrained on natural images, and compare the strength of that transfer with section 43.7's small-base-model example.
- Plot the training and validation loss of the tabular network for every epoch, and find the point (if any) where it starts to overfit.

---

## Recap

- **PyTorch** works with **tensors**, NumPy-like grids of numbers that can keep a record of how they were computed; its default is 32-bit numbers, with about 7 significant digits.
- A **neuron** is a weighted sum plus a bias, passed through an **activation function**: exactly Chapter 37's logistic regression when the activation is the sigmoid.
- **ReLU** avoids the **vanishing gradient** of sigmoid in hidden layers: its slope is 1 for positive inputs, where the sigmoid's is at most 0.25.
- A single neuron can only draw a straight decision boundary; problems like **XOR** need at least one **hidden layer** with a nonlinear activation.
- **Backpropagation** computes the gradient of every parameter with the **chain rule**, working backwards from the loss and reusing each step; PyTorch's **autograd** does it with `.backward()`, and you can check it by hand and with a nudge (in 64-bit numbers).
- On Riverstone's tabular churn data, a small neural network lands in the same range as logistic regression and tuned gradient boosting, and never clearly ahead of boosting: deep learning has no automatic advantage on clean tabular data.
- A **convolution** slides a kernel across an image to produce a **feature map**; **pooling** shrinks it; a CNN learns its kernels, and uses **softmax** and **cross-entropy** for several classes.
- **Transfer learning** reuses a base model's learned features on a new task; its benefit depends on how rich and general the base model's training data was, so compare it with training from scratch, on the same data, over several runs.
- Every deep learning claim should clear the same bar as any other method: beat an honest baseline, measured with the tools from Chapters 36, 37, and 39.

---

## Key terms

PyTorch · tensor · `float32` / `float64` · neuron · activation function · sigmoid · ReLU (rectified linear unit) · tanh · slope of an activation · vanishing gradient · layer · hidden layer · neural network · weight · bias · forward pass · XOR problem · decision boundary · `nn.Sequential` · `nn.Linear` · `BCELoss` / `BCEWithLogitsLoss` · logit · SGD · Adam · epoch · full-batch training · backpropagation · chain rule · autograd · `requires_grad` · numerical gradient check · convolution · kernel (filter) · feature map · padding · pooling (max pooling) · convolutional neural network (CNN) · `nn.Module` · softmax · `CrossEntropyLoss` · learned representation · transfer learning · base task · pretrained model · frozen layers · head · fine-tuning · from-scratch training

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can install PyTorch, make a tensor, and explain why its numbers show long 32-bit tails.
- [ ] I can explain that a single neuron is exactly Chapter 37's logistic regression, with an activation function.
- [ ] I can explain why one neuron cannot solve every classification problem, using XOR as a concrete example.
- [ ] I can compute a small network's forward pass by hand and match it in code.
- [ ] I can compute one backward pass by hand with the chain rule, and I've checked it against autograd and a numerical gradient.
- [ ] I can explain what each line of a PyTorch training step does: `zero_grad`, forward pass, loss, `backward`, `step`.
- [ ] I never assume a neural network beats gradient boosting on tabular data without testing it.
- [ ] I can explain, in plain terms, what a convolution does to an image, and read a feature map.
- [ ] I evaluate an image classifier (or any model) with a proper held-out test, not training accuracy.
- [ ] I know that transfer learning's value depends on what the base model was trained on, and I compare it with training from scratch on the same data before trusting it.
- [ ] I judge every deep learning claim against the same baseline discipline as every other method in this book.

---

## Exercises

Code exercises run in the chapter's notebook after the chapter's code (they use `X_xor`, `y_xor`, `loss_fn`, `X_train`, `Xtr_t`, `ytr_t`, `Xva_t`, `y_valid`, `loss_fn3`, `final_pred`, `base_model`, `SmallCNN`, `to_tensors`, `loss_fn4`, `small_training_set`, `train_transfer`, `train_scratch`, `sweep`, and the rest). Predict each answer before running it.

### Warm-up

1. *(hand)* A neuron has weights [0.4, −0.5], bias 0.2, and input [3, 2]. Compute *z* and then the sigmoid output.
2. *(hand)* Compute ReLU(−3), ReLU(0), and ReLU(4.5).
3. *(hand)* Explain in one sentence why a single neuron cannot solve XOR, without using the word "linear."
4. A network has 2 inputs, one hidden layer of 5 neurons, and 1 output neuron, with biases at every neuron. How many parameters does it have in total? (Show the weights and biases separately.)

### Core

5. Retrain the single neuron on XOR with a much smaller learning rate (`lr=0.01`) for 2,000 steps. Does it now solve XOR? Then keep training it to 20,000 steps. What does that tell you about the difference between "not enough training" and "cannot represent the pattern at all"?
6. Change the two-layer XOR network's hidden layer from 4 neurons to 2. Does it still solve XOR after 3,000 steps? Try 1 hidden neuron. What's the smallest hidden layer that works?
7. Add a third hidden layer to the tabular network (`nn.Linear(8, 8), nn.ReLU()` before the final layer) and retrain for 200 epochs. Does validation AUC improve, get worse, or stay about the same? Relate your answer to Chapter 37's bias–variance discussion.
8. Train the tabular network for 500 epochs instead of 200, printing validation AUC every 50 epochs. Does it keep improving, or does it start to get worse partway through? What would that pattern mean?
9. Retrain the digit CNN using only 200 of the 675 training images (sample them randomly). How much does test accuracy fall? What does this suggest about how much data a from-scratch CNN needs?
10. Extend section 43.7's sweep to `n_per_class` values of 1 and 50, with the same five seeds. Does the pattern continue at both extremes?

### Stretch

11. Write `train_transfer_partial`: like `train_transfer`, but unfreeze `conv2` (keep `conv1` frozen) and fine-tune it along with the new head. At `n_per_class=30`, over the same five seeds, does fine-tuning close the gap with training from scratch?
12. Build a base CNN trained on digits 0–7 (8 classes) instead of 0–4, then transfer it to telling 8 from 9, with 10 examples per class. Compare it, on the same samples and the same test images, with training from scratch and with transferring section 43.6's 0–4 base model. Does a richer base task help?
13. Implement a tiny two-parameter linear model (*y* = *wx* + *b*) in raw PyTorch tensors with `requires_grad=True`, train it with a gradient descent loop you write yourself (no `torch.optim`), and check that it recovers weights close to a `LinearRegression` fit on the same synthetic data.

### Think about it

14. A colleague argues: "Deep learning is state of the art, so we should always use it." Using this chapter's own numbers, write a two-sentence response.
15. Explain to a non-technical stakeholder, in three sentences, why a hidden layer is necessary for a network to learn some patterns, using the XOR example without technical jargon.
16. A vendor says its transfer-learning product was "pretrained on millions of images" and should work well on Riverstone's own product-defect photos. What one question from this chapter would you ask before trusting that claim?

---
## Answers

*Every calculation was checked, and every code output shown is real.*

**1.** *z* = 0.4 × 3 + (−0.5) × 2 + 0.2 = 1.2 − 1.0 + 0.2 = **0.4**. sigmoid(0.4) = 1 ÷ (1 + *e*<sup>−0.4</sup>) = 1 ÷ 1.6703 = **0.599**.

**2.** ReLU(−3) = **0** (negative input, set to 0). ReLU(0) = **0** (exactly at the boundary). ReLU(4.5) = **4.5** (positive input, passed through unchanged).

**3.** A single neuron splits its inputs into two sides with one straight cut, and XOR's two "1" points sit on opposite corners with a "0" point on each of the other two corners, so no single cut can put both 1s on one side and both 0s on the other.

**4.** From input to hidden layer: 2 inputs × 5 hidden neurons = 10 weights, plus 5 biases (one per hidden neuron) = 15 parameters. From hidden to output: 5 hidden neurons × 1 output = 5 weights, plus 1 bias = 6 parameters. **Total: 15 + 6 = 21 parameters.**

**5.**

```python
torch.manual_seed(43)
slow_neuron = nn.Sequential(nn.Linear(2, 1), nn.Sigmoid())
slow_optimizer = torch.optim.SGD(slow_neuron.parameters(), lr=0.01)
for step in range(1, 20001):
    slow_optimizer.zero_grad()
    slow_pred = slow_neuron(X_xor)
    slow_loss = loss_fn(slow_pred, y_xor)
    slow_loss.backward()
    slow_optimizer.step()
    if step in [2000, 5000, 20000]:
        print(
            f"step {step:>5}: loss {slow_loss.item():.4f}   "
            f"predictions {slow_pred.detach().numpy().round(3).ravel()}"
        )
```

```
step  2000: loss 0.6951   predictions [0.548 0.494 0.521 0.467]
step  5000: loss 0.6933   predictions [0.515 0.5   0.504 0.49 ]
step 20000: loss 0.6931   predictions [0.5 0.5 0.5 0.5]
```

No. After 2,000 steps the loss, 0.6951, is slightly *above* ln 2 = 0.6931 and still falling, so this run is on its way to the place the `lr=0.5` run reached; by 20,000 steps it gets there (0.6931, predicting 0.5 for every row) and stops. For a single neuron on XOR, 0.6931 is the best possible loss: both runs head for the same floor, and neither can ever do better. That's the difference. "Not enough training" means the loss is still falling toward a better value; "cannot represent the pattern" means the best possible value is itself no better than guessing, and more steps, or any learning rate, only get you there.

**6.**

```python
for hidden_size in [2, 1]:
    torch.manual_seed(43)
    small_net = nn.Sequential(
        nn.Linear(2, hidden_size), nn.Tanh(), nn.Linear(hidden_size, 1), nn.Sigmoid()
    )
    small_optimizer = torch.optim.SGD(small_net.parameters(), lr=0.5)
    for step in range(3000):
        small_optimizer.zero_grad()
        small_pred = small_net(X_xor)
        small_loss = loss_fn(small_pred, y_xor)
        small_loss.backward()
        small_optimizer.step()
    print(
        f"{hidden_size} hidden neuron(s): loss {small_loss.item():.4f}   "
        f"predictions {small_pred.detach().numpy().round(3).ravel()}"
    )
```

```
2 hidden neuron(s): loss 0.0022   predictions [0.002 0.997 0.997 0.001]
1 hidden neuron(s): loss 0.4799   predictions [0.668 0.665 0.665 0.004]
```

With **2** hidden neurons, the network still solves XOR essentially perfectly (loss 0.0022, predictions [0.002, 0.997, 0.997, 0.001]). With only **1** hidden neuron, it fails (loss 0.4799, predictions of 0.665–0.668 for three of the four points): one hidden neuron is itself a single straight-line boundary feeding the output, so it inherits section 43.2's limitation. **Two is the smallest hidden layer that solves XOR**, matching the picture in Figure 43.1: you need two lines to cut out the diagonal band.

**7.**

```python
torch.manual_seed(43)
deeper_network = nn.Sequential(
    nn.Linear(X_train.shape[1], 16),
    nn.ReLU(),
    nn.Linear(16, 8),
    nn.ReLU(),
    nn.Linear(8, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
)
deeper_optimizer = torch.optim.Adam(deeper_network.parameters(), lr=0.01)
for epoch in range(200):
    deeper_optimizer.zero_grad()
    deeper_loss = loss_fn3(deeper_network(Xtr_t), ytr_t)
    deeper_loss.backward()
    deeper_optimizer.step()
with torch.no_grad():
    deeper_pred = torch.sigmoid(deeper_network(Xva_t)).numpy().ravel()
print(
    f"3 hidden layers: AUC {roc_auc_score(y_valid, deeper_pred):.3f}   "
    f"(2 hidden layers, chapter version: {roc_auc_score(y_valid, final_pred):.3f})"
)
```

```
3 hidden layers: AUC 0.770   (2 hidden layers, chapter version: 0.773)
```

No better: validation AUC 0.770 against the two-layer version's 0.773, a difference well inside the noise of 1,000 validation accounts. With 3,000 training rows and 25 features, the extra layer adds flexibility the data doesn't reward. That's Chapter 37's bias–variance lesson (section 37.10): past a certain point more flexibility adds variance without removing bias, and the way to find that point is to test it, not to assume "deeper is better."

**8.**

```python
torch.manual_seed(43)
long_network = nn.Sequential(
    nn.Linear(X_train.shape[1], 16),
    nn.ReLU(),
    nn.Linear(16, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
)
long_optimizer = torch.optim.Adam(long_network.parameters(), lr=0.01)
for epoch in range(1, 501):
    long_optimizer.zero_grad()
    long_loss = loss_fn3(long_network(Xtr_t), ytr_t)
    long_loss.backward()
    long_optimizer.step()
    if epoch % 50 == 0:
        with torch.no_grad():
            long_pred = torch.sigmoid(long_network(Xva_t)).numpy().ravel()
        print(
            f"after epoch {epoch:>3}: training loss {long_loss.item():.4f}   "
            f"validation AUC {roc_auc_score(y_valid, long_pred):.3f}"
        )
```

```
after epoch  50: training loss 0.2466   validation AUC 0.755
after epoch 100: training loss 0.2375   validation AUC 0.762
after epoch 150: training loss 0.2285   validation AUC 0.771
after epoch 200: training loss 0.2187   validation AUC 0.773
after epoch 250: training loss 0.2088   validation AUC 0.771
after epoch 300: training loss 0.1926   validation AUC 0.761
after epoch 350: training loss 0.1754   validation AUC 0.747
after epoch 400: training loss 0.1609   validation AUC 0.738
after epoch 450: training loss 0.1507   validation AUC 0.734
after epoch 500: training loss 0.1408   validation AUC 0.730
```

Of the checkpoints printed, validation AUC is best after epoch 200 (0.773), then **declines** to 0.730 by epoch 500, while the training loss keeps falling the whole time (0.2466 → 0.1408). Training loss still improving while validation gets worse is the signature of **overfitting**: the network is increasingly memorizing quirks of the 3,000 training rows. In practice this is handled with **early stopping**: check the validation score as you train, and stop (keeping the best weights) once it stops improving, instead of fixing the number of epochs in advance. The true peak could be a few epochs either side of 200; checking more often would find it.

**9.**

```python
small_indices = np.random.default_rng(43).choice(len(Xb_train), 200, replace=False)
Xb_small_t, yb_small_t = to_tensors(Xb_train[small_indices], yb_train[small_indices])
torch.manual_seed(43)
small_data_model = SmallCNN(n_classes=5)
small_optimizer = torch.optim.Adam(small_data_model.parameters(), lr=0.01)
for epoch in range(60):
    small_optimizer.zero_grad()
    small_loss = loss_fn4(small_data_model(Xb_small_t), yb_small_t)
    small_loss.backward()
    small_optimizer.step()
with torch.no_grad():
    small_pred = small_data_model(Xb_test_t).argmax(1)
small_accuracy = (small_pred == yb_test_t).float().mean().item()
print(
    f"200 training images: test accuracy {small_accuracy:.1%}   "
    f"(675 training images, chapter version: {base_accuracy:.1%})"
)
```

```
200 training images: test accuracy 96.9%   (675 training images, chapter version: 98.7%)
```

Test accuracy falls only modestly, from 98.7% with 675 images to 96.9% with 200. This is an easy task (small, clean, centred 8 × 8 digits, only 5 classes), so even a large cut in training data costs little. On harder image problems (more classes, more variation, more noise), a comparable cut usually costs far more, which is why transfer learning and data augmentation matter more in practice than this toy comparison suggests.

**10.**

```python
for n in [1, 50]:
    transfer_runs, scratch_runs = [], []
    for seed in range(5):
        Xs, ys = small_training_set(n, seed)
        transfer_runs.append(train_transfer(Xs, ys, seed))
        scratch_runs.append(train_scratch(Xs, ys, seed))
    t, s = np.array(transfer_runs), np.array(scratch_runs)
    print(
        f"{n:>14}   {t.mean():>9.1%} ({t.min():.0%}-{t.max():.0%})   "
        f"{s.mean():>8.1%} ({s.min():.0%}-{s.max():.0%})"
    )
```

```
             1       58.8% (50%-71%)      65.1% (57%-73%)
            50       95.4% (95%-96%)      97.5% (96%-99%)
```

The same picture continues at both ends: from scratch is ahead at **1** per class (65.1% against 58.8%) and at **50** (97.5% against 95.4%). With one example per digit, both methods are nearly guessing from one exemplar each, and the ranges are wide (50% to 73% across the ten runs), so single runs there could say anything. Across the whole sweep, from 1 to 50 per class, features frozen from this small, narrow base never beat training from scratch on average: the base model simply didn't learn enough to be worth reusing.

**11.**

```python
def train_transfer_partial(Xs, ys, seed, epochs=80):
    torch.manual_seed(seed)
    model = copy.deepcopy(base_model)
    for param in model.conv1.parameters():
        param.requires_grad = False  # conv1 stays frozen; conv2 keeps training
    model.fc1 = nn.Linear(16 * 2 * 2, 32)
    model.fc2 = nn.Linear(32, 5)
    trainable = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.Adam(trainable, lr=0.01)
    for epoch in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn4(model(Xs), ys)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        return (model(Xn_test_t).argmax(1) == yn_test_t).float().mean().item()


partial_runs = [train_transfer_partial(*small_training_set(30, seed), seed) for seed in range(5)]
frozen_runs, scratch_runs = sweep[30]
print(f"n=30, mean of 5 seeds:  conv2 fine-tuned {np.mean(partial_runs):.1%}")
print(f"                        fully frozen     {np.mean(frozen_runs):.1%}")
print(f"                        from scratch     {np.mean(scratch_runs):.1%}")
```

```
n=30, mean of 5 seeds:  conv2 fine-tuned 96.2%
                        fully frozen     94.2%
                        from scratch     96.2%
```

- `train_transfer_partial(*small_training_set(30, seed), seed)`: the `*` unpacks the two tensors that `small_training_set` returns into the first two arguments, as `**` unpacked a dictionary in Chapter 37 (section 37.8).
- `sweep[30]` holds section 43.7's scores for the same five samples.

Fine-tuning `conv2` along with the head (96.2% on average) closes the whole gap between fully frozen features (94.2%) and training from scratch (96.2%) at 30 per class. Letting the later convolution adapt to the new digits, while the first layer's simple edge detectors stay fixed, is standard practice in real transfer learning: freeze the early layers, fine-tune the later ones, and treat how many to unfreeze as a setting to test, not a fixed rule. Here it only draws level with training from scratch, because the base model had little extra to offer.

**12.**

```python
richer_mask = labels < 8  # digits 0-7 as the base task
Xr_train, Xr_test, yr_train, yr_test = train_test_split(
    images[richer_mask], labels[richer_mask], test_size=0.25, random_state=43,
    stratify=labels[richer_mask],
)
Xr_train_t, yr_train_t = to_tensors(Xr_train, yr_train)
torch.manual_seed(43)
richer_base = SmallCNN(n_classes=8)
richer_optimizer = torch.optim.Adam(richer_base.parameters(), lr=0.01)
for epoch in range(60):
    richer_optimizer.zero_grad()
    loss = loss_fn4(richer_base(Xr_train_t), yr_train_t)
    loss.backward()
    richer_optimizer.step()
print(f"8-class base: {len(Xr_train):,} training images")
```

```
8-class base: 1,082 training images
```

```python
final_mask = (labels == 8) | (labels == 9)
Xf_train, Xf_test, yf_train, yf_test = train_test_split(
    images[final_mask], labels[final_mask] - 8, test_size=0.25, random_state=43,
    stratify=labels[final_mask],
)
Xf_test_t, yf_test_t = to_tensors(Xf_test, yf_test)


def sample_8_9(n_per_class, seed):
    rng = np.random.default_rng(seed)
    chosen = []
    for digit_class in [0, 1]:
        candidates = np.where(yf_train == digit_class)[0]
        chosen.extend(rng.choice(candidates, n_per_class, replace=False))
    return to_tensors(Xf_train[chosen], yf_train[chosen])


def train_8_9(Xs, ys, seed, base=None, epochs=80):
    torch.manual_seed(seed)
    if base is None:
        model = SmallCNN(n_classes=2)  # from scratch
    else:
        model = copy.deepcopy(base)
        for param in list(model.conv1.parameters()) + list(model.conv2.parameters()):
            param.requires_grad = False
        model.fc1 = nn.Linear(16 * 2 * 2, 32)
        model.fc2 = nn.Linear(32, 2)
    trainable = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.Adam(trainable, lr=0.01)
    for epoch in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn4(model(Xs), ys)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        return (model(Xf_test_t).argmax(1) == yf_test_t).float().mean().item()


results_8_9 = {"from scratch": [], "transfer from 0-4 base": [], "transfer from 0-7 base": []}
for seed in range(5):
    Xs, ys = sample_8_9(10, seed)
    results_8_9["from scratch"].append(train_8_9(Xs, ys, seed))
    results_8_9["transfer from 0-4 base"].append(train_8_9(Xs, ys, seed, base=base_model))
    results_8_9["transfer from 0-7 base"].append(train_8_9(Xs, ys, seed, base=richer_base))
print(f"8 vs 9, 10 per class, {len(Xf_test)} test images, mean of 5 seeds:")
for name, runs in results_8_9.items():
    print(f"  {name:<24} {np.mean(runs):.1%}  ({min(runs):.0%}-{max(runs):.0%})")
```

```
8 vs 9, 10 per class, 89 test images, mean of 5 seeds:
  from scratch             95.3%  (92%-98%)
  transfer from 0-4 base   93.5%  (90%-96%)
  transfer from 0-7 base   93.9%  (93%-94%)
```

No clear help. With the same five samples of 10 images per class and the same 89 test images, the transfer from the richer 0–7 base (93.9% on average) is a hair above the transfer from the 0–4 base (93.5%), and both are below training from scratch (95.3%). With 89 test images, one image is about 1.1 percentage points, so these three are within a few images of each other. An 8-class base of 1,082 small digits is still a small, narrow base; the rich bases that make transfer learning shine have millions of varied images. The exercise's real lesson is the method: to answer "does a richer base help?" you need the baseline and the other base on the same samples and test set, or the numbers can't be compared.

**13.**

```python
torch.manual_seed(43)
x_data = torch.linspace(0, 10, 50).unsqueeze(1)
y_data = 3.0 * x_data + 7.0 + torch.randn(50, 1) * 0.5  # true line: y = 3x + 7, plus noise

w = torch.zeros(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
learning_rate = 0.01

for step in range(500):
    prediction = x_data * w + b
    loss = ((prediction - y_data) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        w -= learning_rate * w.grad
        b -= learning_rate * b.grad
        w.grad.zero_()
        b.grad.zero_()

print(f"manual gradient descent: w={w.item():.3f}   b={b.item():.3f}")

from sklearn.linear_model import LinearRegression

sklearn_fit = LinearRegression().fit(x_data.numpy(), y_data.numpy())
print(
    f"scikit-learn LinearRegression: w={sklearn_fit.coef_[0, 0]:.3f}"
    f"   b={sklearn_fit.intercept_[0]:.3f}"
)
```

```
manual gradient descent: w=3.102   b=6.382
scikit-learn LinearRegression: w=3.027   b=6.885
```

The loop you wrote (w = 3.102, b = 6.382) lands close to the true values (w = 3, b = 7) and to scikit-learn's least-squares fit (w = 3.027, b = 6.885), but not exactly on the fit, because 500 gradient-descent steps (Chapter 35) haven't fully reached the minimum that `LinearRegression`'s exact formula (Chapter 37, section 37.1) finds directly; with 2,000 steps the loop matches the fit to three decimals. The update happens inside `torch.no_grad()` because changing a weight is not part of the model's calculation, so PyTorch mustn't record it. And `.grad.zero_()` matters exactly as `optimizer.zero_grad()` did throughout the chapter: without it, each step's gradients would be added to the previous ones. What the exercise confirms: a "neural network" with no hidden layer and no activation function is just linear regression, trained by gradient descent instead of solved by formula.

**14.** "This chapter's own numbers say otherwise on tabular data: on our churn accounts, a small neural network scored in the same range as plain logistic regression and tuned gradient boosting, and never clearly beat boosting, while needing far more code and tuning than either. 'State of the art' is true for images, text, and audio at scale; it isn't automatically true for a table of account features, and the only way to know which situation you're in is to test it, the same way we test everything else."

**15.** "Imagine sorting four boxes into two piles using only one straight cut of a knife: some arrangements can't be separated that way, wherever you cut. A single artificial 'neuron' can only make one such straight cut. Adding a hidden layer is like being allowed to make two cuts and then combine the results, which handles arrangements no single cut ever could."

**16.** "What was the base model actually trained on, and how similar is that to our product-defect photos?" This chapter's own experiment showed transfer learning's value depends on how rich and relevant the base model's training data is. A model pretrained on millions of *everyday* photographs (cats, cars, landscapes) may transfer only partly to a specific defect-spotting task, and the only way to know is to test the vendor's actual model on a held-out sample of Riverstone's own photos, compared with a simpler baseline, exactly as Chapter 39 would insist for any model.

---

## Where this leads

- **Chapter 37, Supervised Learning Algorithms,** is this chapter's constant point of comparison: logistic regression and gradient boosting, both still very much in play.
- **Chapter 39, Evaluation, Tuning, Interpretation & Honesty,** governs how any deep learning result should be judged, unchanged.
- **Chapter 41, NLP Foundations,** previewed learned representations with word embeddings; Chapter 54 scales that idea up enormously.
- **Chapter 53, Deep Learning in Depth,** goes further into architectures, regularization, and training at scale.
- **Chapter 54, Generative AI & Large Language Models,** is where transfer learning's real power shows up: models pretrained on vastly larger, richer data than anything in this chapter.
- **Interview preparation:** the Machine Learning Question Bank (Chapter 74) covers backpropagation, activation functions, why XOR needs a hidden layer, and "when would you use deep learning versus a simpler model?" — one of the most common questions in applied ML interviews, and one this chapter now lets you answer with evidence.
