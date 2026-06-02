### 1. Problemas de Física e Lógica



* **Atrito Dinâmico Nulo na Transição:** O maior problema do código está no método `forca_atrito_est`. Se a massa está parada (`v_rel == 0`), mas a força de inércia rompe o atrito estático (`abs(Fat) > Fat_lim`), a função retorna a força de atrito dinâmico multiplicando por `-np.sign(v_rel)`. Como `v_rel` é 0, a função `np.sign(0)` retorna 0. Isso significa que, no exato passo de tempo em que a massa descola, ela sofre atrito zero, em vez de sofrer um atrito oposto à força de inércia.  
    ---> Isso não é um problema pq eu nunca passo a v_rel mas sim a direcao da velocidade. O método foi fatorado para refletir essa mudança

* **Perda de Contato (Força Normal Negativa):** Você calcula a normal com `N.append(-P + ms*ay[i])`. Se a aceleração vertical `ay` for muito negativa (por exemplo, a calha acelerando para baixo mais rápido que a gravidade), a Força Normal se tornará negativa. O código não verifica se $N \le 0$. Se isso acontecer na vida real, a massa "voa" (perde contato), e o atrito deveria ser estritamente zero, mas seu código vai gerar limites de atrito negativos ou invertidos.
    ---> RESOLVIDO

* **Cálculo da Condição de Descolamento:** Ao descolar da calha (dentro do bloco `if(d_vel_x == 0)` e `fat[0] == -1`), você define `d_vel_x = ax[i]/abs(ax[i])`. No entanto, a direção da velocidade relativa inicial deveria ser oposta à aceleração da calha, já que a massa tende a ficar para trás pela inércia. O uso direto da aceleração para definir o sentido do atrito pode gerar sinais invertidos dependendo do seu sistema de coordenadas.
    ---> RESOLVIDO

---

### 2. Problemas Numéricos e de Algoritmo

* **Integração Numérica Básica (Euler):** Você está calculando a velocidade com `v_rel[i-1] + (t[i] - t[i-1])*(a_rel)`. Esse é o método de Euler explícito. Para sinais de vibração com mudanças rápidas (como os gerados por uma `CubicSpline`), o método de Euler de primeira ordem acumula erros rapidamente (drift). Pode ser necessário usar um método mais robusto (como Runge-Kutta) ou diminuir muito o passo de tempo.
    ---> TROCAR EULER POR RUNGE-KUTTA

* **Tratamento de "Zero-Crossing" (Cruzamento por Zero):** Quando a massa para em relação à calha, você detecta a mudança de sinal da velocidade (`(v_rel[i-1] * v_rel[i]) < 0`) e simplesmente zera a velocidade atual (`v_rel[i] = 0`). Embora funcione para evitar que a massa oscile infinitamente, isso descarta a fração do passo de tempo antes de parar, causando uma ligeira perda de precisão e de energia no sistema.

---

### 3. Qualidade de Código e Boas Práticas

* **Nomenclatura Confusa de Variáveis:** Você declarou `ms` para a massa (0.001 kg), `mu_s` para o coeficiente dinâmico (no escopo de `vel_atr`), e `m_s` para o coeficiente dinâmico (como parâmetro de `forca_atrito_est`). Ter `ms` e `m_s` na mesma assinatura de função é perigoso, confuso para leitura e altamente suscetível a erros de digitação.
* **Dependências e Funções Ausentes:** Funções como `sinal_estatico()`, `modulo()`, `_print()` e `_input()` são chamadas, mas não estão definidas no escopo apresentado. O mesmo vale para bibliotecas como `numpy` (`np`), `matplotlib.pyplot` (`plt`) e classes do `scipy` (`CubicSpline`, `integrate`).
