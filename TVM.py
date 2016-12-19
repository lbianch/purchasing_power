import math

class TVM:
    """Time value of money calculator
    
    Arguments:
        n (int): number of periods
        r (float): interest rate per period as decimal not percent
        pv (float): present value in arbitrary monetary units
        pmt (float): payment amount per period
        fv (float): future value in arbitrary monetary units
        mode (str) (optional): select begin or end mode; valid values are 'BEGIN' and 'END'
        
    Attributes:
        See Arguments
        
    """
    def __init__(self, n=0, r=0.0, pv=0.0, pmt=0.0, fv=0.0, mode='END'):
        self.n = n
        self.r = r
        self.pv = pv
        self.pmt = pmt
        self.fv = fv
        self.mode = mode.upper()
        if mode not in ('BEGIN', 'END'):
            raise ValueError("Mode must be 'BEGIN' or 'END'")

    def __str__(self):
        return "n={self.n}, r={self.r}, pv={self.pv}, fv={self.fv}, pmt={self.pmt}, mode={self.mode}".format(self=self)
    
    def __repr__(self):
        return "TVM({})".format(str(self))

    def _is_begin_mode(self):
        return self.mode == 'BEGIN'

    def calc_pv(self):
        """Calculates the present value using n, r, pmt, and fv.
        
        Returns:
            float: present value
        """
        z = math.pow(1.0 + self.r, -self.n)
        pva = self.pmt / self.r
        if self._is_begin_mode(): 
            pva += self.pmt
        return -(self.fv * z + (1.0 - z) * pva)

    def calc_fv(self, r=None):
        """Calculates the future value using n, r, pmt, and pv
        
        Parameters:
            r (float) (optional): Specify an overriding interest rate
        
        Returns:
            float: future value
        """
        r = r or self.r
        z = math.pow(1.0 + r, -self.n)
        pva = self.pmt / r
        if self._is_begin_mode(): 
            pva += self.pmt
        return -(self.pv + (1.0 - z) * pva) / z

    def calc_pmt(self):
        """Calculates the payment per period using n, r, pv, and fv
        
        Returns:
            float: payment per period
        """
        z = math.pow(1.0 + self.r, -self.n)
        pmt = (self.pv + self.fv * z) * self.r / (z - 1.0)
        if self._is_begin_mode():
            pmt /= (1.0 + self.r)
        return pmt

    def calc_n(self):
        """Calculates the number of periods using r, pmt, pv, and fv
        
        Returns:
            float: number of periods; non-integer results are to be
                   interpreted as requiring the floor of the result
                   plus a fraction of a period
        """
        pva = self.pmt / self.r
        if self._is_begin_mode(): 
            pva += self.pmt
        z = -(pva + self.pv) / (self.fv - pva)
        return -math.log(z) / math.log(1.0 + self.r)

    def calc_r(self):
        """Calculates the rate using n, pmt, pv, and fv
        
        Returns:
            float: interest rate per period as a decimal; multiply by
                   100 to obtain a percent and multiply by the periods 
                   per year to obtain an APR
        """
        r = 0.05
        r0 = r
        maxIter = 1000
        minError = 10.0**-4
        def delta(r):
            return self.calc_fv(r) - self.fv
        def slope(r):
            return (delta(r * r0) - delta(r)) / (r * r0)
        for _ in range(maxIter):
            r -= delta(r) / slope(r)
            if abs(self.calc_fv(r) - self.fv) < minError: 
                return r
        raise ValueError("No solution for r could be found for {self}".format(self=self)) 

def pv(n, r, pmt, fv, mode='END'):
    return TVM(n=n, r=r, pv=0.0, pmt=pmt, fv=fv, mode=mode).calc_pv()

def fv(n, r, pmt, pv, mode='END'):
    return TVM(n=n, r=r, pv=pv, pmt=pmt, fv=0.0, mode=mode).calc_fv()

def pmt(n, r, pv, fv, mode='END'):
    return TVM(n=n, r=r, pv=pv, pmt=0.0, fv=fv, mode=mode).calc_pmt()

def r(n, pv, pmt, fv, mode='END'):
    return TVM(n=n, r=0.0, pv=pv, pmt=pmt, fv=fv, mode=mode).calc_r()

def n(r, pv, pmt, fv, mode='END'):
    return TVM(n=0.0, r=r, pv=pv, pmt=pmt, fv=fv, mode=mode).calc_n()

def mortgage_payment(years, rate, amount):
    """Calculate a monthly mortgage payment 
    
    Arguments:
        years (int): number of years for the mortgage
        rate (float): interest rate; rates above 0.25 are assumed to be percentages
                      eg, rate = 0.2 or 20 would be 20% but rate = 2 would be 2%
        amount (float): value of the mortgage, in base currency units
                        values under 10,000 are assumed to be in thousands, eg,
                        1000 means 1 million but 150,000 is 150,000
        
    Returns:
        float: monthly payment for the mortgage in base currency units (see amount)
    """
    # Assume mortgage rates do not drop below 0.25%
    if rate > 0.25:
        rate /= 100.0
    # Assume mortgage amounts under 10,000 are in thousands:
    if amount < 10000.0:
        amount *= 1000.0
    return pmt(n=years*12.0, r=rate/12.0, pv=-amount, fv=0.0)

