export interface Task {
    id: string;
    name: string;
    description: string;
    category: 'development' | 'testing' | 'documentation' | 'deployment';
    complexity: 'low' | 'medium' | 'high';
    duration: number;
    start_date?: string;
    end_date?: string;
    dependencies: string[];
    start_day?: number;
  }
  
  export interface ProjectPlan {
    tasks: Task[];
    total_duration: number;
    dependencies: Record<string, string[]>;
    start_date?: string;
    end_date?: string;
    outputs?: {
      markdown?: string;
      json?: any;
      gantt?: string;
    };
  }
  
  export interface ProjectResponse extends ProjectPlan {
    id?: number;
    description: string;
    created_at?: string;
  }