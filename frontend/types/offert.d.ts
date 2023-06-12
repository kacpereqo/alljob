type EmploymentType =
  | "b2b"
  | "permanent"
  | "mandate"
  | "contract"
  | "internship"
  | "part_time"
  | "other";

declare global {
  interface LeadingOffert {
    _id: string;
    title: string;
    createdAt: string;
    locations: string[];
    technologies: string[];
    employment_type: EmploymentType;
    company: {
      name: string;
      url: string;
      logo_url: string;
    };
  }
}

export {};
