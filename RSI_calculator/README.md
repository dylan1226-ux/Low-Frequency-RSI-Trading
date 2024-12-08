### 1. Overbought and Oversold Strategy

#### **Idea**:
When RSI is above 70, it indicates a potential overbought condition, suggesting a price pullback might occur. When RSI is below 30, it indicates a potential oversold condition, suggesting a price rebound might occur.
#### Buy Signal:
Buy when RSI rises above 30 after being below 30.
#### Sell Signal:
Sell when RSI falls below 70 after being above 70.
#### Exit Signals:
1. **Return to Neutral Zone**: Exit when RSI moves back to the neutral zone:  
   - From the oversold zone <30 to above 50, or  
   - From the overbought zone >70 to below 50.  
2. **Fixed Holding Period**: Exit after holding the position for a fixed period (e.g., n days).

### 2. RSI Countertrend Trading Strategy
#### **Strategy**:
**Buy** when:  

$$
RSI_t - RSI_{t-k} < -a
$$

**Sell** when:  

$$
RSI_t - RSI_{t-k} > a
$$

#### Exit Criteria:
Exit when momentum regresses toward zero or after n days.
