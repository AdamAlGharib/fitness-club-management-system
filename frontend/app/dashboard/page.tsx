'use client'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Dumbbell, Calendar, Users, TrendingUp, Clock, Award, Activity, Target, ChevronRight, LogOut } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function DashboardPage() {
  const router = useRouter()

  const handleSignOut = () => {
    router.push('/')
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
                <Dumbbell className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">FitForce</h1>
                <p className="text-xs text-muted-foreground">Member Portal</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Badge variant="secondary" className="px-3 py-1">
                Premium Member
              </Badge>
              <Button variant="ghost" size="sm" onClick={handleSignOut}>
                <LogOut className="h-4 w-4 mr-2" />
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-2">Welcome back, Alex!</h2>
          <p className="text-muted-foreground">Ready to crush your fitness goals today?</p>
        </div>

        {/* Stats Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
          <Card className="border-2 hover:border-accent transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Workouts This Week
              </CardTitle>
              <Activity className="h-4 w-4 text-accent" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground">12</div>
              <p className="text-xs text-muted-foreground mt-1">
                <span className="text-accent font-medium">+3</span> from last week
              </p>
            </CardContent>
          </Card>

          <Card className="border-2 hover:border-accent transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Total Hours
              </CardTitle>
              <Clock className="h-4 w-4 text-accent" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground">24.5</div>
              <p className="text-xs text-muted-foreground mt-1">
                <span className="text-accent font-medium">+5.2h</span> this month
              </p>
            </CardContent>
          </Card>

          <Card className="border-2 hover:border-accent transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Calories Burned
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-accent" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground">8,420</div>
              <p className="text-xs text-muted-foreground mt-1">
                Average <span className="text-accent font-medium">702/day</span>
              </p>
            </CardContent>
          </Card>

          <Card className="border-2 hover:border-accent transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Achievements
              </CardTitle>
              <Award className="h-4 w-4 text-accent" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground">18</div>
              <p className="text-xs text-muted-foreground mt-1">
                <span className="text-accent font-medium">2 new</span> this week
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Services Grid */}
        <div className="grid gap-6 lg:grid-cols-2 mb-8">
          <Card className="border-2">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-xl">Personal Training</CardTitle>
                  <CardDescription>One-on-one sessions with expert trainers</CardDescription>
                </div>
                <div className="h-12 w-12 rounded-lg bg-accent/10 flex items-center justify-center">
                  <Users className="h-6 w-6 text-accent" />
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Sessions Remaining</span>
                  <span className="font-semibold text-foreground">8 / 12</span>
                </div>
                <div className="h-2 rounded-full bg-muted overflow-hidden">
                  <div className="h-full bg-accent" style={{ width: '67%' }} />
                </div>
              </div>
              <div className="pt-2">
                <p className="text-sm text-muted-foreground mb-3">Your assigned trainer:</p>
                <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                  <div className="h-10 w-10 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-semibold">
                    MJ
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold text-foreground text-sm">Mike Johnson</p>
                    <p className="text-xs text-muted-foreground">Strength & Conditioning</p>
                  </div>
                  <Badge variant="outline" className="text-xs">Pro</Badge>
                </div>
              </div>
              <Button className="w-full" variant="outline">
                <Calendar className="h-4 w-4 mr-2" />
                Book Next Session
              </Button>
            </CardContent>
          </Card>

          <Card className="border-2">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-xl">Group Classes</CardTitle>
                  <CardDescription>Join high-energy group workouts</CardDescription>
                </div>
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Dumbbell className="h-6 w-6 text-primary" />
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                {[
                  { name: 'HIIT Training', time: 'Today, 6:00 PM', spots: '3 spots left' },
                  { name: 'Yoga Flow', time: 'Tomorrow, 8:00 AM', spots: '5 spots left' },
                  { name: 'Spin Class', time: 'Tomorrow, 7:00 PM', spots: 'Full' },
                ].map((classItem, i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-muted rounded-lg hover:bg-muted/70 transition-colors cursor-pointer group">
                    <div>
                      <p className="font-semibold text-foreground text-sm group-hover:text-accent transition-colors">
                        {classItem.name}
                      </p>
                      <p className="text-xs text-muted-foreground">{classItem.time}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-muted-foreground">{classItem.spots}</span>
                      <ChevronRight className="h-4 w-4 text-muted-foreground group-hover:text-accent transition-colors" />
                    </div>
                  </div>
                ))}
              </div>
              <Button className="w-full">
                View All Classes
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Additional Services */}
        <Card className="border-2">
          <CardHeader>
            <CardTitle className="text-xl">More Services</CardTitle>
            <CardDescription>Explore everything FitForce has to offer</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <button className="flex flex-col items-start p-4 rounded-lg border-2 border-border hover:border-accent transition-colors group text-left">
                <Target className="h-8 w-8 text-accent mb-3" />
                <h3 className="font-semibold text-foreground mb-1 group-hover:text-accent transition-colors">
                  Nutrition Plans
                </h3>
                <p className="text-sm text-muted-foreground">
                  Custom meal plans designed for your goals
                </p>
              </button>

              <button className="flex flex-col items-start p-4 rounded-lg border-2 border-border hover:border-accent transition-colors group text-left">
                <Activity className="h-8 w-8 text-accent mb-3" />
                <h3 className="font-semibold text-foreground mb-1 group-hover:text-accent transition-colors">
                  Body Assessments
                </h3>
                <p className="text-sm text-muted-foreground">
                  Track progress with regular body composition scans
                </p>
              </button>

              <button className="flex flex-col items-start p-4 rounded-lg border-2 border-border hover:border-accent transition-colors group text-left">
                <Award className="h-8 w-8 text-accent mb-3" />
                <h3 className="font-semibold text-foreground mb-1 group-hover:text-accent transition-colors">
                  Challenges
                </h3>
                <p className="text-sm text-muted-foreground">
                  Compete with members and earn rewards
                </p>
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
