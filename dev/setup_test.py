import os 
import sys

def main():
    sys.path.append("//Users/andrewliu/Documents/exp_proj/flexure_exp_proj/src")
    from FT232H import pll_reader
        
    pll = pll_reader()
    pll.pll_read()


if __name__ == '__main__':
    main()