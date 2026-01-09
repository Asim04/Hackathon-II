// User interface
export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

// Auth session interface
export interface AuthSession {
  user: User;
  token: string;
  expiresAt: string;
}

// Sign up input interface
export interface SignUpInput {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

// Sign in input interface
export interface SignInInput {
  email: string;
  password: string;
}