// Not yet optimised...

#if __VERSION__ < 130

float tanh(float x) {
    if (x < -12.0) {
        return -1.0;
    }
    if (x > 12.0) {
        return 1.0;
    }
    float p = exp(2.0*x);
    return (p-1.0)/(p+1.0);
}

float cosh(float x) {
    float p = exp(2.0*x);
    return (1.0+p)/(2.0*p);
}

#endif

vec2 ctimes(vec2 a, vec2 b) {
    return mat2(a, -a.y, a.x)*b;
}

vec2 cexp(vec2 a) {
    float r = exp(a.x);
    return r*vec2(cos(a.y), sin(a.y));
}

void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
    const int N = 256;
    // Bands towards lower left and right are "aliasing" due to the sampling used
    // in the integration. Nump up M to improve.
    // M needs to be odd.
#define M 197
    float rate = 0.005;
    
    //float xmin = -60.0;
    //float xmax = 60.0;
    float xmax = 20.0+iMouse.x/iResolution.x*80.0;
    float xmin = -xmax;
    float ymax = xmax+15.0;
    float ymin = xmin+15.0;
    //float ymin = -30.0;
    //float ymax = 90.0;
    
    float gamma = -3.75+5.75*sin(iTime);
    
	vec2 uv = fragCoord.xy / iResolution.xy;
    
    float alpha = ymin+uv.y*(ymax-ymin);
    float beta = xmin+uv.x*(xmax-xmin);

    //int k;
    vec2 integral = vec2(0.0, 0.0);
    
    float coeff;
    int odd = 1;
    float x = -4.0;
    float dx = 8.0/float(M);
    for (int k = 0; k <= M; ++k) {
        odd = 1-odd;
        // Simpson's integration rule
        if (k == 0 || k == M) {
            coeff = 1.0;
        } else {
            if (odd == 1) {
                coeff = 4.0;
            } else {
                coeff = 2.0;
            }
        }
        float x2 = x*x;
        float x3 = x*x2;
        float x4 = x*x3;
        
        float u = rate*(5.0*x4+3.0*gamma*x2+2.0*beta*x+alpha);
    	float y = tanh(u);
        
        vec2 z = vec2(x, y);
        vec2 z2 = ctimes(z, z);
        vec2 z3 = ctimes(z2, z);
        vec2 z4 = ctimes(z3, z);
        vec2 z5 = ctimes(z4, z);

        vec2 f = z5+gamma*z3+beta*z2+alpha*z;
		vec2 g = cexp(vec2(-f.y, f.x));
       
        float d = cosh(u);
        vec2 dz = dx*vec2(1.0, rate*(20.0*x3+6.0*gamma*x+2.0*beta)/(d*d));      

 		integral += coeff*ctimes(g, dz);

        
     	x += dx;
   }
   
    float value = 0.5*length(integral)/(3.0);
    
    fragColor = vec4(value);
}
