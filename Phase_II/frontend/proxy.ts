import { NextRequest, NextResponse } from 'next/server';

// Define protected routes
const protectedRoutes = ['/dashboard'];
const authRoutes = ['/auth/signin', '/auth/signup'];

export function proxy(request: NextRequest) {
  // Check for auth token in cookies
  const token = request.cookies.get('better-auth-session-token');

  // If user is trying to access protected route without token
  if (protectedRoutes.some(route => request.nextUrl.pathname.startsWith(route)) && !token) {
    // Redirect to sign in
    return NextResponse.redirect(new URL('/auth/signin', request.url));
  }

  // If user is authenticated and trying to access auth routes, redirect to dashboard
  if (authRoutes.some(route => request.nextUrl.pathname.startsWith(route)) && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Continue with the request
  return NextResponse.next();
}

// Configure which routes the proxy should run for
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
