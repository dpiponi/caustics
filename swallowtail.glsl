// Not yet optimised...
// For use at Shadertoy

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

vec2 ctimes(vec2 a, vec2 b) {
    return vec2(a.x*b.x-a.y*b.y, a.x*b.y+a.y*b.x);
}

vec2 cexp(vec2 a) {
    float r = exp(a.x);
    return vec2(r*cos(a.y), r*sin(a.y));
}

void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
    const int N = 256;
#define M 257
    float rate = 0.005;
    
    float xmin = -30.0;
    float xmax = 30.0;
    float ymin = -20.0;
    float ymax = 50.0;
    
    float gamma = -3.75+3.75*sin(iTime);
    
	vec2 uv = fragCoord.xy / iResolution.xy;
    
    float alpha = ymin+uv.y*(ymax-ymin);
    float beta = xmin+uv.x*(xmax-xmin);

    //int k;
    vec2 integral = vec2(0.0, 0.0);
    
    float coeff;
    int odd = 1;
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
    	float x = -12.0+24.0*float(k)/float(M);
    	float y = tanh(rate*(5.0*x*x*x*x+3.0*gamma*x*x+2.0*beta*x+alpha));
        
        vec2 z = vec2(x, y);
        vec2 z2 = ctimes(z, z);
        vec2 z3 = ctimes(z2, z);
        vec2 z4 = ctimes(z3, z);
        vec2 z5 = ctimes(z4, z);

        vec2 f = z5+gamma*z3+beta*z2+alpha*z;
		vec2 g = cexp(vec2(-f.y, f.x));
        
        float d = cosh(rate*(5.0*x*x*x*x+3.0*gamma*x*x+2.0*beta*x+alpha));
        vec2 dz = vec2(1.0, rate*(20.0*x*x*x+6.0*gamma*x+2.0*beta)/(d*d));
        
        integral += coeff*g;
    }
   
    float value = 0.05*length(integral/3.0);
    
    fragColor = vec4(value, value, value, 1.0);
}
