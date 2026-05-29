import time

# Step 1: Print blank lines to reserve space in the terminal 
# so the cursor has room to move up on the first iteration.
# (We have 3 lines of output, so we print 3 newlines)
print("\n\n\n") 

for k in range(1, 5):
    # Step 2: Build the output string
    # \033[3A moves the cursor UP exactly 3 lines.
    output = "\033[3A" 
    
    # Step 3: Add each line. 
    # \033[K clears the line from the cursor to the right margin before writing.
    output += f"\033[KCalculating node: {k}\n"
    output += f"\033[KDisplacement: {k * 0.5} mm\n"
    output += f"\033[KStatus: Solving..."
    
    # Step 4: Print the whole block at once. 
    # end="" prevents an extra newline, flush=True forces the terminal to draw it instantly.
    print(output, end="", flush=True)
    time.sleep(0.5)

print("\n\nAnalysis complete.") # Move past the block when done
