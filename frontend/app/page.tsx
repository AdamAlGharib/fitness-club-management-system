'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dumbbell, Mail, Lock, User } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function SignInPage() {
  const router = useRouter()
  const [activeTab, setActiveTab] = useState('signin')
  const [role, setRole] = useState<'member' | 'trainer' | 'admin'>('member')

  const handleSignIn = (e: React.FormEvent) => {
    e.preventDefault()
    // Simulate sign in - in production, this would authenticate with a backend
    router.push('/dashboard')
  }

  const handleSignUp = (e: React.FormEvent) => {
    e.preventDefault()
    // Simulate sign up - in production, this would create a user account
    router.push('/dashboard')
  }

  return (
    <div className="min-h-screen flex">
      {/* Left side - Hero section */}
      <div className="hidden lg:flex lg:flex-1 relative overflow-hidden bg-primary">
        <div className="absolute inset-0 bg-[url('/athletic-person-training-in-modern-gym.jpg')] bg-cover bg-center opacity-20" />
        <div className="relative z-10 flex flex-col justify-between p-12 text-primary-foreground">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-accent">
              <Dumbbell className="h-7 w-7 text-accent-foreground" />
            </div>
            <span className="text-2xl font-bold tracking-tight">FitForce</span>
          </div>
          
          <div className="space-y-6 max-w-md">
            <h1 className="text-5xl font-bold leading-tight text-balance">
              Transform Your Body & Mind
            </h1>
            <p className="text-lg text-primary-foreground/90 leading-relaxed">
              Join our community of fitness enthusiasts. Expert trainers, premium equipment, and a supportive environment to help you reach your goals.
            </p>
            <div className="flex gap-8 pt-4">
              <div>
                <div className="text-3xl font-bold">2,500+</div>
                <div className="text-sm text-primary-foreground/80">Active Members</div>
              </div>
              <div>
                <div className="text-3xl font-bold">50+</div>
                <div className="text-sm text-primary-foreground/80">Expert Trainers</div>
              </div>
              <div>
                <div className="text-3xl font-bold">15</div>
                <div className="text-sm text-primary-foreground/80">Years Experience</div>
              </div>
            </div>
          </div>

          <div className="text-sm text-primary-foreground/70">
            © 2025 FitForce Gym. All rights reserved.
          </div>
        </div>
      </div>

      {/* Right side - Sign in form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-background">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center space-y-2 lg:hidden">
            <div className="flex justify-center mb-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-primary">
                <Dumbbell className="h-8 w-8 text-primary-foreground" />
              </div>
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-foreground">FitForce</h2>
          </div>

          <Card className="border-2">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl font-bold text-center">Welcome Back</CardTitle>
              <CardDescription className="text-center">
                Sign in to access your fitness journey
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="signin">Sign In</TabsTrigger>
                  <TabsTrigger value="signup">Sign Up</TabsTrigger>
                </TabsList>

                <TabsContent value="signin" className="space-y-4">
                  <form onSubmit={handleSignIn} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="email"
                          type="email"
                          placeholder="you@example.com"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password">Password</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="password"
                          type="password"
                          placeholder="••••••••"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="role">Sign in as</Label>
                      <select
                        id="role"
                        value={role}
                        onChange={(e) => setRole(e.target.value as 'member' | 'trainer' | 'admin')}
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      >
                        <option value="member">Member</option>
                        <option value="trainer">Trainer</option>
                        <option value="admin">Admin Staff</option>
                      </select>
                    </div>

                    <div className="flex items-center justify-between text-sm">
                      <label className="flex items-center gap-2 cursor-pointer">
                        <input type="checkbox" className="rounded border-input" />
                        <span className="text-muted-foreground">Remember me</span>
                      </label>
                      <a href="#" className="text-accent hover:underline font-medium">
                        Forgot password?
                      </a>
                    </div>

                    <Button type="submit" className="w-full" size="lg">
                      Sign In
                    </Button>
                  </form>
                </TabsContent>

                <TabsContent value="signup" className="space-y-4">
                  <form onSubmit={handleSignUp} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="signup-name">Full Name</Label>
                      <div className="relative">
                        <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="signup-name"
                          type="text"
                          placeholder="John Doe"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="signup-email">Email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="signup-email"
                          type="email"
                          placeholder="you@example.com"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="signup-password">Password</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                        <Input
                          id="signup-password"
                          type="password"
                          placeholder="••••••••"
                          className="pl-10"
                          required
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="signup-role">Join as</Label>
                      <select
                        id="signup-role"
                        value={role}
                        onChange={(e) => setRole(e.target.value as 'member' | 'trainer' | 'admin')}
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      >
                        <option value="member">Member</option>
                        <option value="trainer">Trainer</option>
                      </select>
                    </div>

                    <Button type="submit" className="w-full" size="lg">
                      Create Account
                    </Button>

                    <p className="text-xs text-center text-muted-foreground">
                      By signing up, you agree to our Terms of Service and Privacy Policy
                    </p>
                  </form>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          <p className="text-center text-sm text-muted-foreground">
            Need help? <a href="#" className="text-accent hover:underline font-medium">Contact support</a>
          </p>
        </div>
      </div>
    </div>
  )
}
