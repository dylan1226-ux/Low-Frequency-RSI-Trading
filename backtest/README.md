## Rebalancing Frequency
**Daily**

## Initial Capital
**10 million CNY**

---

## Trading Signals

**Overbought/Oversold Strategy (Signal 1)**

**RSI Reversal Trading Strategy (Signal 2)**

---

## Position Management

- **Initial Account Asset**:  
  initCap = 10 million CNY

- **Daily Trading Allocation**:  
  ALLOCATION = 10 million CNY

- **Contract Value Calculation**:  
  Adjust position size based on the signals.

---

## Strategy Description

### **Trading Signal Calculation**
- Use daily closing prices to calculate signals.
- **Signal 1**:
  - When RSI exceeds 30, generate a **buy** signal.
  - When RSI drops below 70, generate a **sell** signal.
- **Signal 2**:
  - Generate **buy** or **sell** signals based on RSI difference strategy.

### **Position Management**
- **Signal 1 and Signal 2** are managed as **separate positions**, tracked and calculated independently.
- **Initial Account Capital**: 10 million CNY.
- **Daily Maximum Trading Allocation**: 10 million CNY.

#### **Signal 1 Management**
1. On a **buy signal**, purchase a fixed number `P` of IC main contracts at the closing price.
2. On a **sell signal**, sell a fixed number of IC main contracts at the closing price.
3. On an **exit signal**, sell half of the Signal 1 position.

#### **Signal 2 Management**
1. On a **buy signal**, purchase a fixed number of IC main contracts at the closing price.
2. On a **sell signal**, sell a fixed number of IC main contracts at the closing price.
3. On an **exit signal**, sell half of the Signal 2 position.

---

### **Daily Position Adjustment**
- **Expected Position Calculation**:

$$
P = \frac{\text{ALLOCATION}}{\text{Contract Value}} 
$$

- For **long positions**:

$$
P = \frac{\text{ALLOCATION}}{\text{Contract Value}} 
$$

- For **short positions**:

$$
P = -\frac{\text{ALLOCATION}}{\text{Contract Value}} 
$$

---

## Return Calculation

- **Daily Return**:  

$$
\text{Daily Return} = \frac{\text{(Today's Close Price - Yesterday's Close Price) × Position Size}}{\text{Initial Capital}}
$$

- **Total Return**:  
  Accumulated daily returns.

---

## Calculation Steps

- **Contract Details**:
  - **Multiplier**: 5
  - **Minimum Tick Size**: 2 CNY

- **Determine Minimum Price Adjustment Unit (Min Size)**:  
  2 CNY

- **Determine Contract Multiplier**:  
  5

- **Determine Minimum Tick Adjustment**:  
  2 CNY

- **Slippage Cost**:  
  Slippage cost is calculated as:
  
$$
\text{SlippageCost} = \text{slippage} \times \text{n} \times \text{multiplier} \times \text{mintick}
$$

- **Total Cost**:
  
$$ 
\text{Total Cost} = (\text{Current Price} \times \text{Contract Multiplier}) + \text{Trading Costs}
$$
